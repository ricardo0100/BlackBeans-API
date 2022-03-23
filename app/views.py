from audioop import cross
from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy import null
from app import app, api, db
from app.model import Account, Category, Bean, User
from flask_httpauth import HTTPTokenAuth
from flask_cors import cross_origin
import hashlib
import time
import uuid

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    return User.query.filter(User.token == token).first()


@app.route("/")
def home():
    return "Welcome to Earth"


# User
@app.route("/login", methods=['POST'])
def login():
    email = request.form['email'].lower()
    password = sha256_hash(request.form['password'])
    user = User.query.filter(User.email == email, User.password == password).first_or_404()
    return user.serialize()


@app.route("/signup", methods=['POST'])
def signup():
    email = request.form['email'].lower()
    password = sha256_hash(request.form['password'])
    name = request.form['name']
    token = str(uuid.uuid4())
    if User.query.filter(User.email == email).first() is not None:
        return None
    user = User()
    user.name = name
    user.email = email
    user.password = password
    user.token = token
    user.creation = time.time()
    user.update = time.time()
    db.session.add(user)
    db.session.commit()
    return user.serialize()


def sha256_hash(string):
    sha256 = hashlib.sha256()
    sha256.update(string.encode('utf-8'))
    return sha256.hexdigest()


# Account
class AccountsListResource(Resource):
    @staticmethod
    # @auth.login_required
    def get():
        after_timestamp = request.args.get('updated_after')
        if (after_timestamp is None): 
            after_timestamp = 0
        accounts = Account.query.filter(Account.update >= after_timestamp).all()
        response_body = jsonify(list(map(lambda account: account.serialize(), accounts)))
        response = make_response(response_body)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    @staticmethod
    @auth.login_required
    def post():
        json = request.json
        account = Account()
        account.name = json["name"]
        account.update = json["lastSavedTime"]
        account.creation = json["createdTime"]
        account.isActive = True
        db.session.add(account)
        db.session.commit()
        return account.serialize()


class AccountsResource(Resource):
    @staticmethod
    @auth.login_required
    def get(account_id):
        return jsonify(Account.query.get(account_id).serialize())

    @staticmethod
    @auth.login_required
    def put(account_id):
        account = Account.query.get(account_id)
        json = request.json
        account.name = json["name"]
        account.update = json["lastSavedTime"]
        account.isActive = json["isActive"]
        db.session.commit()
        return account.serialize()


# Category
class CategoryListResource(Resource):
    @staticmethod
    @auth.login_required
    def get():
        after_timestamp = request.args.get('updated_after')
        categories = Category.query.filter(Category.update >= after_timestamp).all()
        return jsonify(list(map(lambda category: category.serialize(), categories)))

    @staticmethod
    @auth.login_required
    def post():
        json = request.json
        category = Category()
        category.name = json["name"]
        category.update = json["lastSavedTime"]
        category.creation = json["createdTime"]
        category.isActive = True
        db.session.add(category)
        db.session.commit()
        return category.serialize()


class CategoriesResource(Resource):
    @staticmethod
    @auth.login_required
    def get(category_id):
        return jsonify(Category.query.get(category_id).serialize())

    @staticmethod
    @auth.login_required
    def put(category_id):
        category = Category.query.get(category_id)
        json = request.json
        category.name = json["name"]
        category.update = json["lastSavedTime"]
        category.isActive = json["isActive"]
        db.session.commit()
        return category.serialize()


# Bean
class BeanListResource(Resource):
    @staticmethod
    @auth.login_required
    def get():
        after_timestamp = request.args.get('updated_after')
        beans = Bean.query.filter(Bean.update >= after_timestamp).all()
        return jsonify(list(map(lambda bean: bean.serialize(), beans)))

    @staticmethod
    @auth.login_required
    def post():
        json = request.json
        bean = Bean()
        bean.name = json["name"]
        bean.update = json["lastSavedTime"]
        bean.creation = json["createdTime"]
        bean.effectivation = json["effectivationTime"]
        bean.value = json["value"]
        bean.isCredit = json["isCredit"]
        bean.isActive = True
        bean.category_id = json.get("categoryID", None)
        bean.account_id = json["accountID"]
        db.session.add(bean)
        db.session.commit()
        return bean.serialize()


class BeanResource(Resource):
    @staticmethod
    @auth.login_required
    def get(bean_id):
        return jsonify(Bean.query.get(bean_id).serialize())

    @staticmethod
    @auth.login_required
    def put(bean_id):
        bean = Bean.query.get(bean_id)
        json = request.json
        bean.name = json["name"]
        bean.update = json["lastSavedTime"]
        bean.effectivation = json["effectivationTime"]
        bean.value = json["value"]
        bean.isCredit = json["isCredit"]
        bean.isActive = json["isActive"]
        bean.category_id = json.get("categoryID", None)
        bean.account_id = json["accountID"]
        db.session.commit()
        return bean.serialize()


# Paths
api.add_resource(AccountsListResource, "/accounts")
api.add_resource(AccountsResource, "/account/<int:account_id>")

api.add_resource(CategoryListResource, "/categories")
api.add_resource(CategoriesResource, "/category/<int:category_id>")

api.add_resource(BeanListResource, "/beans")
api.add_resource(BeanResource, "/bean/<int:bean_id>")
