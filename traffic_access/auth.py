"""
Routes of authentication in this app.

AUTHOR: Keiber Urbila
CREATION DATE: 10/06/21
"""
from flask import Blueprint, render_template, request, flash, redirect, \
    url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from modules.auth import is_safe_url
from .models import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """ Login route """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials. please check and try again.")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)

        if request.form.get("next") != "None":
            next_page = request.form.get("next")
        else:
            next_page = False

        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next_page):
            return abort(400)
        return redirect(next_page or url_for('trends.index'))

    return render_template("login_form.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password_check = request.form.get("password_check")

        # Email validator
        if len(email.partition("@")[0]) < 4:
            flash("Email username must be at least 4 characters long.")
            return redirect(url_for("auth.signup"))

        # Password validator
        if password != password_check:
            flash("Passwords do not match.")
            return render_template("signup_form.html")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("User already exists.")
            return redirect(url_for("auth.signup"))

        new_user = User(username=email.partition("@")[0],
                        email=email,
                        password=generate_password_hash(password,
                                                        method="sha256"))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup_form.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
