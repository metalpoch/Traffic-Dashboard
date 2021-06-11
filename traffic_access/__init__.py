'''
Start web app Traffic Access.

AUTHOR: Keiber Urbila
CREATE DATE: 06/06/2021
'''
from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from .views import trends
from .config import DB_URI, SECRET_KEY, DIR_DOCUMENTS

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)
fa = FontAwesome(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = ""

login_manager.init_app(app)

from .models import User


@login_manager.user_loader
def load_user(user_id):
    """ Since the user_id is just the primary key of use it in the query for
    the user """
    return User.query.get(int(user_id))


from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


app.register_blueprint(trends)


@app.route('/cv')
def show_cv():
    return send_from_directory(DIR_DOCUMENTS, "KeiberUrbila-CV.pdf")
