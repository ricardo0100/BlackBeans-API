from flask import jsonify, request
from flask_restful import Resource
from app import app, api, db
from app.model import Account, Category


@app.route("/")
def home():
    return "BlackBeans 🐶<br><a href='https://github.com/ricardo0100/BlackBeansAPI'>Github page</a>"


# Accounts
class AccountsListResource(Resource):
    @staticmethod
    def get():
        return jsonify(list(map(lambda account: account.serialize(), Account.query.all())))

    @staticmethod
    def post():
        json = request.json
        account = Account()
        account.name = json["name"]
        account.update = json["update"]
        account.creation = json["creation"]
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
        account.update = json["update"]
        db.session.commit()
        return account.serialize()


api.add_resource(AccountsListResource, "/account")
api.add_resource(AccountsResource, "/account/<int:account_id>")
