"""
Simple config and credentials for this app.

AUTHOR: Keiber Urbila
CREATION DATE: 10/06/21
"""
from os import path
from secrets import token_urlsafe


DIR_BASE = path.dirname(__file__)
DIR_DOCUMENTS = path.join(DIR_BASE, "static", "documents")
DB_URI = f"sqlite:///{path.join(DIR_BASE, 'db.sqlite')}"
SECRET_KEY = token_urlsafe()
