'''
pip install flask-sqlalchemy, flask-login, flask-bcrypt
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
# versão local
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
# após o deploy
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = "e752b3fb63c15d68ff0ea6f9051a9c7c"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts" # armazenar fotos dos usuarios nessa pasta específica

# BASE DE DADOS
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"


from fakepinterest import routes