from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import json

with open('flask_todo/config.json', 'r') as config_file:
    config_json = json.load(config_file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = config_json['DB_URL']
app.config['SECRET_KEY']= config_json['App_Secret_Key'] 
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from flask_todo import routes
