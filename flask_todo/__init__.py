from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///todo.db'
app.config['SECRET_KEY']= 'SECRETKEY'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from flask_todo import routes