"""
Routes from traffic_charts route

AUTHOR: Keiber Urbila
CREATION DATE: 10/06/21
"""
import io
import pandas as pd
from modules import query_db
from modules.trend import chart_trend, get_dataframe_pivoted_by_date
from flask import render_template, request, session, url_for, redirect, \
    make_response, Blueprint
from flask_login import login_required


def validate_form(city: str, company: str, firstday: str, lastday: str):
    """ Validate form and save query as session """
    data_form = {"city": city, "company": company}

    if firstday is None:
        session["firstday"] = "2021-04-01"
    else:
        session["firstday"] = firstday

    if lastday is None:
        session["lastday"] = "2021-04-07"
    else:
        session["lastday"] = lastday

    for index, value in data_form.items():
        try:
            session[index] = value if value is not None else session[index]

        except KeyError:  # if session dont exist. Create a session null
            session[index] = None
            print(f"was error with {index}: {value}")


trends = Blueprint("trends", __name__)


@trends.route("/")
@login_required
def index():
    """ Homepage for trends route """

    validate_form(request.args.get("city"),
                  request.args.get("company"),
                  request.args.get("firstday"),
                  request.args.get("lastday"))

    if session["city"] is None:
        return render_template("layout_trends.html",
                               zip=zip,
                               lastday=session["lastday"],
                               firstday=session["firstday"])

    measurements = query_db.Measurements(session["city"],
                                         firstday=session["firstday"],
                                         lastday=session["lastday"])

    # get df from trends in database
    df = measurements.get_trend(session["company"])

    del measurements  # del object of memory

    graph_json = chart_trend(data=df.copy(),
                             city=session["city"],
                             company=session['company'].title())

    try:
        df, dates, elements = get_dataframe_pivoted_by_date(df=df,
                                                            date_list=True,
                                                            element_list=True,
                                                            add_suffix=True)
    except ValueError:
        return render_template("layout_trends.html",
                               zip=zip,
                               lastday=session["lastday"],
                               firstday=session["firstday"])

    return render_template("layout_trends.html",
                           column_names=dates,
                           elements_name=elements,
                           graph_json=graph_json,
                           row_data=list(df.values.tolist()),
                           city=session["city"],
                           company=session["company"],
                           zip=zip,
                           lastday=session["lastday"],
                           firstday=session["firstday"])


@trends.route("/clean")
def clean_sessions():
    """ Clean all session saved """
    for i in ("city", "company", "firstday", "lastday"):
        try:
            session.pop(i, None)
        except KeyError:  # if session dont exist
            pass

    return redirect(url_for("trends.index"))


@trends.route("/download")
@login_required
def download():
    " Download file excel with the values shown in the HTML table"
    measurements = query_db.Measurements(session["city"],
                                         firstday=session["firstday"],
                                         lastday=session["lastday"])

    # get df from trends in database
    df = measurements.get_trend(session["company"])

    if session.get("subgroup"):
        df = df[df["Element"].str.startswith(session["subgroup"])]
        session.pop("subgroup")

    del measurements  # del object of memory

    df, _, _ = get_dataframe_pivoted_by_date(df=df,
                                             date_list=False,
                                             element_list=False,
                                             add_suffix=False)
    # Instantiate byte type IO object, used to store object in memory
    out = io.BytesIO()

    # Create sheet_name
    writer = pd.ExcelWriter(out, engine="xlsxwriter")

    sheetname = "Sheet"

    df.to_excel(writer, sheet_name=sheetname)

    # Auto length for columns
    for column in df:
        column_length = max(df[column].astype(str).map(len).max(),
                            len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheetname].set_column(col_idx, col_idx, column_length)

    # Save df excel in the memory writer variable, do not include number index
    writer.save()

    # Reset the pointer of the IO object to the beginning
    out.seek(0)

    # The IO object uses get value() to return the binary raw data.
    resp = make_response(out.getvalue())

    # Set the response header to let browser resolve to the file download
    # behavior.
    resp.headers["Content-Disposition"] = (
        f"attachment; filename={session['city']}_{session['company']}.xlsx"
    )
    resp.headers["Content-Type"] = "application/vnd.ms-excel; charset=utf-8"
    return resp
