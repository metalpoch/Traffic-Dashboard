"""
Model of database for this apps.
Date range for the trends is between "2021-03-29 23:55" and "2021-04-27 22:59".

AUTHOR: Keiber Urbila
CREATION DATE: 10/06/21
"""
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
