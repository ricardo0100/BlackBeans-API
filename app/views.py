from flask import jsonify, request
from flask_restful import Resource
from app import app, api, db
from app.model import Account, Category


@app.route("/")
def home():
    return "BlackBeans 🐶<br/><a href='https://github.com/ricardo0100/BlackBeansAPI'>Github page</a>"


# Account
class AccountsListResource(Resource):
    @staticmethod
    def get():
        after_timestamp = request.args.get('updated_after')
        accounts = Account.query.filter(Account.update >= after_timestamp).all()
        return jsonify(list(map(lambda account: account.serialize(), accounts)))

    @staticmethod
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
    def get(account_id):
        return jsonify(Account.query.get(account_id).serialize())

    @staticmethod
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
    def get():
        after_timestamp = request.args.get('updated_after')
        categories = Category.query.filter(Category.update >= after_timestamp).all()
        return jsonify(list(map(lambda category: category.serialize(), categories)))

    @staticmethod
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
    def get(category_id):
        return jsonify(Category.query.get(category_id).serialize())

    @staticmethod
    def put(category_id):
        category = Category.query.get(category_id)
        json = request.json
        category.name = json["name"]
        category.update = json["lastSavedTime"]
        category.isActive = json["isActive"]
        db.session.commit()
        return category.serialize()


# Paths
api.add_resource(AccountsListResource, "/account")
api.add_resource(AccountsResource, "/account/<int:account_id>")

api.add_resource(CategoryListResource, "/category")
api.add_resource(CategoriesResource, "/category/<int:category_id>")
