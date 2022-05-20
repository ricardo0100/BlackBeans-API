from flask import jsonify, make_response, redirect, request, render_template, url_for
import flask_login
from flask_restful import Resource
from application import app, api, db
from application.model import Account, Category, Bean, User
from flask_login import login_user, logout_user, login_required
import hashlib
import time
import uuid


def verify_token(token):
    return User.query.filter(User.token == token).first()


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/app")
@login_required
def frontend_app():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = sha256_hash(request.form['password'])
        user = User.query.filter(
            User.email == email, User.password == password).first()
        login_user(user)
        return redirect(url_for('frontend_app'))
    else:
        return render_template('login.html')


@app.route('/api/test')
def test_login():
    user = User.query.filter(User.id == 1).first_or_404()
    login_user(user)
    return redirect('http://127.0.0.1:3000')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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
    def get(account_id):
        user = flask_login.current_user
        return jsonify(Account.query.filter(Account.id == account_id, Account.user_id == user.id).first_or_404().serialize())

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


Category


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

#     @staticmethod
#     def post():
#         json = request.json
#         category = Category()
#         category.name = json["name"]
#         category.update = json["lastSavedTime"]
#         category.creation = json["createdTime"]
#         category.isActive = True
#         db.session.add(category)
#         db.session.commit()
#         return category.serialize()


# class CategoriesResource(Resource):
#     @staticmethod
#     def get(category_id):
#         return jsonify(Category.query.get(category_id).serialize())

#     @staticmethod
#     def put(category_id):
#         category = Category.query.get(category_id)
#         json = request.json
#         category.name = json["name"]
#         category.update = json["lastSavedTime"]
#         category.isActive = json["isActive"]
#         db.session.commit()
#         return category.serialize()


# # Bean
# class BeanListResource(Resource):
#     @staticmethod
#     def get():
#         after_timestamp = request.args.get('updated_after')
#         beans = Bean.query.filter(Bean.update >= after_timestamp).all()
#         return jsonify(list(map(lambda bean: bean.serialize(), beans)))

#     @staticmethod
#     def post():
#         json = request.json
#         bean = Bean()
#         bean.name = json["name"]
#         bean.update = json["lastSavedTime"]
#         bean.creation = json["createdTime"]
#         bean.effectivation = json["effectivationTime"]
#         bean.value = json["value"]
#         bean.isCredit = json["isCredit"]
#         bean.isActive = True
#         bean.category_id = json.get("categoryID", None)
#         bean.account_id = json["accountID"]
#         db.session.add(bean)
#         db.session.commit()
#         return bean.serialize()


# class BeanResource(Resource):
#     @staticmethod
#     def get(bean_id):
#         return jsonify(Bean.query.get(bean_id).serialize())

#     @staticmethod
#     def put(bean_id):
#         bean = Bean.query.get(bean_id)
#         json = request.json
#         bean.name = json["name"]
#         bean.update = json["lastSavedTime"]
#         bean.effectivation = json["effectivationTime"]
#         bean.value = json["value"]
#         bean.isCredit = json["isCredit"]
#         bean.isActive = json["isActive"]
#         bean.category_id = json.get("categoryID", None)
#         bean.account_id = json["accountID"]
#         db.session.commit()
#         return bean.serialize()


# Paths
api.add_resource(AccountsListResource, "/api/accounts")
api.add_resource(AccountsResource, "/api/account/<int:account_id>")

api.add_resource(CategoryListResource, "/api/categories")
# api.add_resource(CategoriesResource, "/api/category/<int:category_id>")

# api.add_resource(BeanListResource, "/api/beans")
# api.add_resource(BeanResource, "/api/bean/<int:bean_id>")
