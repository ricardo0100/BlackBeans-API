from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost:3306/black_beans"
# db = SQLAlchemy(app)


# from app import model
from app import views


