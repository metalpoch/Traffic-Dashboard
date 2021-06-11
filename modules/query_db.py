"""
Get trends of element in database.

AUTHOR: Keiber Urbila
CREATE DATE: 10/06/2021
"""
# import pymysql
import pandas as pd
from sqlalchemy import create_engine
from traffic_access.config import DB_URI


class Measurements:
    """
    Query database and get required data
    """

    def __init__(self, city: str, firstday: str, lastday: str):
        self.city = city
        self.firstday = firstday
        self.lastday = lastday
        self.engine = create_engine(DB_URI)

    def get_trend(self, apps: str):
        """
        Return a dataframe from the database with trends by apps and city.

        apps: str -> Apps to filter query.
        """
        if apps == "google":
            and_where = "AND app IN ('Google', 'Youtube', 'Gmail', 'Drive')"
        elif apps == "facebook":
            and_where = """AND app IN ('Facebook', 'Messenger',
            'Whatsapp', 'Instagram')"""
        elif apps == "microsoft":
            and_where = "AND app IN ('Microsoft 365', 'Outlook', 'Skype')"
        elif apps == "others":
            and_where = """AND app IN ('Discord', 'Twitter',
            'Wikipedia', 'Telegram', 'Mercado Libre')"""
        else:
            and_where = ""

        request_sql = f"""SELECT *
        FROM trend
        WHERE (Time BETWEEN '{self.firstday}'
        AND '{self.lastday} 23:59:59' AND
        `City` = '{self.city}'
        {and_where})
        """

        return pd.read_sql(request_sql, self.engine)
