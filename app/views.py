from flask import jsonify, request
from flask_restful import Resource
from app import app, api, db
from app.model import Account, Category, Bean, User
from flask_httpauth import HTTPTokenAuth
import hashlib

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    print("TOKEN: " + token)
    return User.query.filter(User.token == token).first()


@app.route("/")
@auth.login_required
def home():
    return "Welcome " + auth.current_user().name


# User
@app.route("/login", methods=['POST'])
def login():
    email = request.form['email'].lower()
    password = request.form['password']
    h = hashlib.sha256()
    h.update(password.encode('utf-8'))
    password_hash = h.hexdigest()
    user = User.query.filter(User.email == email, User.password == password_hash).first_or_404()
    return user.serialize()


# Account
class AccountsListResource(Resource):
    @staticmethod
    @auth.login_required
    def get():
        after_timestamp = request.args.get('updated_after')
        accounts = Account.query.filter(Account.update >= after_timestamp).all()
        return jsonify(list(map(lambda account: account.serialize(), accounts)))

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
api.add_resource(AccountsListResource, "/account")
api.add_resource(AccountsResource, "/account/<int:account_id>")

api.add_resource(CategoryListResource, "/category")
api.add_resource(CategoriesResource, "/category/<int:category_id>")

api.add_resource(BeanListResource, "/bean")
api.add_resource(BeanResource, "/bean/<int:bean_id>")
