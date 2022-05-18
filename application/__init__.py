import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager

app = Flask(__name__,
            static_url_path='/assets/',
            static_folder='templates/assets/',
            template_folder='templates/')

app.secret_key = b'c3bef16dbaf2c0004740c9d0b4bd9cf23c639a5d8a68b4a435fc20bb7f3eca31'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'MYSQL_URI', 'mysql://root@localhost:3306/black_beans')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return model.User.query.filter(model.User.id == user_id).first()


db = SQLAlchemy(app)
api = Api(app)

from application import model
from application import views

db.create_all()
db.session.commit()
