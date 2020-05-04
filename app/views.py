# from flask import jsonify, request
# from flask_restful import Resource, Api
from app import app#, db
# from app.model import Account

# api = Api(app)
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
# Accounts


# class AccountsListResource(Resource):
#     @staticmethod
#     def get():
#         return jsonify(list(map(lambda account: account.serialize(), Account.query.all())))
#
#
# api.add_resource(AccountsListResource, "/account")
#
#
# class AccountsResource(Resource):
#     @staticmethod
#     def get(account_id):
#         return jsonify(Account.query.get(account_id).serialize())
#
#     @staticmethod
#     def put(account_id):
#         account = Account.query.get(account_id)
#         json = request.json
#         account.name = json["name"]
#         db.session.commit()
#         return account.serialize()
#
#
# api.add_resource(AccountsResource, "/account/<int:account_id>")