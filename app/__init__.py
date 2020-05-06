import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("MYSQL_URI", "mysql://root@localhost:3306/black_beans")
db = SQLAlchemy(app)
api = Api(app)

from app import model
from app import views
