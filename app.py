from flask import Flask, request
from flask_restful import reqparse, abort, Resource, Api

app = Flask(__name__)
api = Api(app)

accounts = [
    {"id": 1, "name": "Bank of Saint Denis"},
    {"id": 2, "name": "Banco do Brasil"}
]

@app.route("/")
def index():
    return "BlackBeans API"

def findAccount(id):
    for account in accounts:
        if account["id"] == id:
            return account

class Account(Resource):
    def get(self, id):
        return findAccount(id)

    def put(self, id):
        account = request.json
        accounts.append(account)
        return findAccount(id)

class AccountList(Resource):
    def get(self):
        return accounts

api.add_resource(AccountList, "/account")
api.add_resource(Account, "/account/<int:id>")

if __name__ == "__main__":
    app.run(debug=False)
