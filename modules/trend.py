"""
Module with the logic of the calculations of the application "trends"

AUTHOR: Keiber Urbila
CREATE DATE: 10/06/2021
"""
import json
import pandas as pd
import plotly
import plotly.graph_objects as go


def add_suffix_in_the_header_of_excel_file(df):
    """ Rename "Bits In/Out" columns from the larger value in this columns. """

    if df["Bits Max"].median() >= 10**9 < 10**12:
        for col in ["Bits In", "Bits Out"]:
            df[col] = (df[col] / 10**9).round(2)
            rename = {"Bits In": "In (Gbps)", "Bits Out": "Out (Gbps)"}
            value_suffix = ["In (Gbps)", "Out (Gbps)"]

    elif df["Bits Max"].median() >= 10**6 < 10**9:
        for col in ["Bits In", "Bits Out"]:
            df[col] = (df[col] / 10**6).round(2)
            rename = {"Bits In": "In (Mbps)", "Bits Out": "Out (Mbps)"}
            value_suffix = ["In (Mbps)", "Out (Mbps)"]

    elif df["Bits Max"].median() >= 10**3 < 10**6:
        for col in ["Bits In", "Bits Out"]:
            df[col] = (df[col] / 10**3).round(2)
            rename = {"Bits In": "In (Kbps)", "Bits Out": "Out (Kbps)"}
            value_suffix = ["In (Kbps)", "Out (Kbps)"]
    else:
        rename = {"Bits In": "Bits In", "Bits Out": "Bits Out"}
        value_suffix = ["Bits In", "Bits Out"]

    df.rename(columns=rename, inplace=True)
    return df.pivot_table(index="App",
                          columns="Time",
                          values=value_suffix,
                          aggfunc="sum")


def get_dataframe_pivoted_by_date(df,
                                  date_list: bool,
                                  element_list: bool,
                                  add_suffix: bool):
    """
    Create and export the next dataframe BUT only show the values. Export a
    element list and date list.

    | App | Date 1| Date 2 | Date n |
    |_____|_in|out|_in|out_|_in|out_|
    | abc | 1 | 3 | 2 | 9  | 1 | 8  |"""

    try:
        df["Time"] = pd.to_datetime(
            df["Time"], format="%Y%m%d %H").dt.strftime("%d-%B-%Y")
    except ValueError:
        df["Time"] = pd.to_datetime(
            df["Time"], format="%Y%m%d%H").dt.strftime("%d-%B-%Y")

    date_list = pd.unique(df["Time"]).tolist() if date_list else None

    df = df.groupby(["Time", "App"])[["Bits In",
                                      "Bits Out"]].max().reset_index()

    if add_suffix:
        # Add SI sufix in Bits In/Out
        for i in ["Bits In", "Bits Out"]:
            df[i] = df[i].apply(
                lambda x: f"{round(x, 2)}" if x < 10**3 else(
                    f"{round(x/10**3, 2)}K" if x < 10**6 else (
                        f"{round(x/10**6, 2)}M" if x < 10**9 else(
                            f"{round(x/10**9, 2)}G")
                    )))
        df = df.pivot_table(index="App",
                            columns="Time",
                            values=["Bits In", "Bits Out"],
                            aggfunc="sum")

    else:
        df["Bits Max"] = df[["Bits In", "Bits Out"]].max(axis=1)
        df = add_suffix_in_the_header_of_excel_file(df)

    element_list = df.index.tolist() if element_list else None

    # Resort column after pivot_table
    df.columns = df.columns.swaplevel(0, 1)
    df.sort_index(axis=1, level=0, inplace=True)

    return df, date_list, element_list


def pre_chart(data):
    """
    export sum of all elements bits in/out into df
    """
    # Ignore backup elements
    data['Time'] = pd.to_datetime(data['Time']).dt.strftime('%Y%m%d%H')
    data["Bits"] = data[["Bits In", "Bits Out"]].max(axis=1)
    data = data.groupby(["Time", "App"])["Bits"].sum().reset_index()
    data["Time"] = pd.to_datetime(data["Time"], format='%Y%m%d%H')

    return data


def chart_trend(data, city: str, company: str):
    """ Create and return chart area plotly and return json

    data: Dataframe.
    city: str -> City of aside in the HTML and database.
    type_app: str -> company of apps.
    """

    data = data[data["City"] == city]
    data = pre_chart(data)

    fig = go.Figure()

    apps = data["App"].unique().tolist()
    for app in apps:
        filter_data = data[["Time", "Bits"]][data["App"] == app]
        fig.add_trace(go.Scatter(x=filter_data["Time"],
                                 y=filter_data["Bits"],
                                 name=app,
                                 mode='lines',
                                 line=dict(width=3)))
        del filter_data

    fig.update_layout(yaxis_title="Consumo",
                      yaxis_tickformat='s',
                      xaxis={'title': 'Fecha',
                             'visible': True,
                             'showticklabels': True},
                      title=f"{company} apps in {city}",
                      hovermode='x',
                      height=400,
                      paper_bgcolor='rgb(38, 41, 51)',
                      plot_bgcolor='rgb(38, 41, 51)',
                      font=dict(color='rgb(154,167,179)', size=12))

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json
