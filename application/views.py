import flask_login
import hashlib
import time
import uuid
from flask import jsonify, make_response, redirect, request, render_template, url_for
from flask_restful import Resource
from application import app, api, db
from application.model import Account, Category, Item, User
from flask_login import login_user, logout_user, login_required
from sqlalchemy import false, select
from sqlalchemy.orm import aliased


def verify_token(token):
    return User.query.filter(User.token == token).first()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/login", methods=['POST'])
def api_login():
    email = request.json['email'].lower()
    password = sha256_hash(request.json['password'])
    user = User.query.filter(
        User.email == email, User.password == password).first_or_404()
    login_user(user)
    return user.serialize()


# @app.route('/api/test')
# def test_login():
#     user = User.query.filter(User.id == 1).first_or_404()
#     login_user(user)
#     user = flask_login.current_user
#     return redirect('http://127.0.0.1:3000')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].lower()
        password = sha256_hash(request.form['password'])
        token = str(uuid.uuid4())
        if User.query.filter(User.email == email).first() is not None:
            return "E-mail already in use"
        user = User()
        user.name = name
        user.email = email
        user.password = password
        user.token = token
        user.creation = time.time()
        user.update = time.time()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('frontend_app'))
    else:
        return render_template('register.html')


# API

@app.route('/api/user')
@login_required
def current_user():
    return {'name': 'Ricardo'}


# Resources
@app.route("/api/available-colors", methods=['GET'])
@login_required
def colors():
    colors = {
        "colors": [
            '#0d6efd',
            '#6610f2',
            '#6f42c1',
            '#d63384',
            '#dc3545',
            '#fd7e14',
            '#ffc107',
            '#198754',
            '#20c997',
            '#0dcaf0',
            '#adb5bd',
        ]
    }
    return colors


@app.route("/api/available-icons", methods=['GET'])
@login_required
def icons():
    icons = {
        "icons": [
            'house',
            'shopping_cart',
            'directions_car',
            'flight',
            'fastfood',
            'restaurant_menu',
            'pets',
            'school',
            'construction',
            'local_shipping',
            'local_taxi',
            'festival',
            'atm',
            'computer',
            'fitness_center',
            'child_friendly',
            'beach_access',
            'savings',
            'rocket_launch',
            'anchor',
            'outdoor_grill',
            'wallet',
            'local_bar',
            'local_post_office',
            'sailing',
            'liquor',
            'church',
            'attractions',
            'local_movies',
            'subway',
            'kitchen',
            'free_breakfast',
            'chair',
            'bed',
            'pedal_bike',
        ]
    }
    return icons


def sha256_hash(string):
    sha256 = hashlib.sha256()
    sha256.update(string.encode('utf-8'))
    return sha256.hexdigest()


# Account
class AccountsListResource(Resource):
    @staticmethod
    @login_required
    def get():
        user = flask_login.current_user
        accounts = Account.query.filter(
            Account.is_active == True,
            Account.user_id == user.id
        ).all()
        response_body = jsonify(
            list(map(lambda row: row.serialize(), accounts))
        )
        response = make_response(response_body)
        return response

    @staticmethod
    @login_required
    def post():
        user = flask_login.current_user
        json = request.json
        account = Account()
        account.user_id = user.id
        account.name = json["name"]
        account.color = json["color"]
        account.update = json["lastSavedTime"]
        account.creation = json["createdTime"]
        account.is_active = True
        db.session.add(account)
        db.session.commit()
        return account.serialize()


class AccountsResource(Resource):
    @staticmethod
    @login_required
    def put(account_id):
        user = flask_login.current_user
        account = Account.query.filter(
            Account.id == account_id, Account.user_id == user.id).first_or_404()
        json = request.json
        account.name = json["name"]
        account.color = json['color']
        account.update = json["lastSavedTime"]
        account.is_active = json["isActive"]
        db.session.commit()
        return account.serialize()

    @staticmethod
    @login_required
    def delete(account_id):
        user = flask_login.current_user
        account = Account.query.filter(
            Account.id == account_id, Account.user_id == user.id).first_or_404()
        account.is_active = False
        db.session.commit()
        return 200


# Category
class CategoryListResource(Resource):
    @staticmethod
    @login_required
    def get():
        user = flask_login.current_user
        categories = Category.query.filter(
            Category.is_active == True,
            Category.user_id == user.id
        ).all()
        return jsonify(list(map(lambda category: category.serialize(), categories)))

    @staticmethod
    def post():
        user = flask_login.current_user
        json = request.json
        category = Category()
        category.user_id = user.id
        category.name = json["name"]
        category.color = json["color"]
        category.icon = json["icon"]
        category.update = json["lastSavedTime"]
        category.creation = json["createdTime"]
        category.is_active = True
        db.session.add(category)
        db.session.commit()
        return category.serialize()


class CategoriesResource(Resource):
    @staticmethod
    def put(category_id):
        user = flask_login.current_user
        category = Category.query.filter(
            Category.id == category_id, Category.user_id == user.id).first_or_404()
        json = request.json
        category.name = json["name"]
        category.color = json["color"]
        category.icon = json["icon"]
        category.update = json["lastSavedTime"]
        category.is_active = json["isActive"]
        db.session.commit()
        return category.serialize()

    @staticmethod
    @login_required
    def delete(category_id):
        user = flask_login.current_user
        account = Category.query.filter(
            Category.id == category_id, Category.user_id == user.id).first_or_404()
        account.is_active = False
        db.session.commit()
        return 200


# Item
class ItemListResource(Resource):
    @staticmethod
    def get():
        user = flask_login.current_user
        stmt = select(
            Item,
            Account,
            Category
        )\
            .join(Account)\
            .outerjoin(Category)\
            .filter(
                Item.user_id == user.id,
                Item.is_active == True,
                Account.is_active == True
        )\
            .order_by(Item.id)
        items = db.session.execute(stmt).all()

        def serialize_row(item):
            dict = {
                "id": item[0].id,
                "name": item[0].name,
                "value": item[0].value,
                "isCredit": item[0].is_credit,
                "date": item[0].date,
                "account": {
                    "id": item[1].id,
                    "name": item[1].name,
                    "color": item[1].color
                }
            }
            if (item[2] != None):
                dict["category"] = {
                    "id": item[2].id,
                    "name": item[2].name,
                    "color": item[2].color,
                    "icon": item[2].icon
                }

            return dict

        return jsonify(list(map(lambda item: serialize_row(item), items)))

    @staticmethod
    def post():
        user = flask_login.current_user
        json = request.json
        item = Item()
        item.user_id = user.id
        item.name = json["name"]
        item.date = json["date"]
        item.value = json["value"]
        item.is_credit = json["isCredit"]
        item.is_active = True
        item.category_id = json.get("categoryId", None)
        item.account_id = json["accountId"]
        db.session.add(item)
        db.session.commit()
        return item.serialize()


class ItemResource(Resource):
    @staticmethod
    def put(item_id):
        user = flask_login.current_user
        item = Item.query.filter(
            Item.id == item_id, Item.user_id == user.id).first_or_404()
        json = request.json
        item.name = json["name"]
        item.date = json["date"]
        item.value = json["value"]
        item.isCredit = json["isCredit"]
        item.isActive = json["isActive"]
        item.category_id = json.get("categoryId", None)
        item.account_id = json["accountId"]
        db.session.commit()
        return item.serialize()

    @staticmethod
    def delete(item_id):
        user = flask_login.current_user
        item = Item.query.filter(
            Item.id == item_id, Item.user_id == user.id).first_or_404()
        item.is_active = False
        db.session.commit()
        return 200


# Paths
api.add_resource(AccountsListResource, "/api/accounts")
api.add_resource(AccountsResource, "/api/account/<int:account_id>")

api.add_resource(CategoryListResource, "/api/categories")
api.add_resource(CategoriesResource, "/api/category/<int:category_id>")

api.add_resource(ItemListResource, "/api/items")
api.add_resource(ItemResource, "/api/item/<int:item_id>")


@app.route("/api/dashboard", methods=['GET'])
def dashboard():
    user = flask_login.current_user
    accounts = Account.query.filter(
        Account.is_active == True,
        Account.user_id == user.id
    ).all()

    categories = Category.query.filter(
        Account.is_active == True,
        Account.user_id == user.id
    ).all()

    return {
        "accountsBoard": list(map(lambda row: row.serialize(), accounts)),
        "categoriesChart": list(map(lambda row: row.serialize(), categories))
    }
