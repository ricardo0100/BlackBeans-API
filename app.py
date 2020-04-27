from flask import Flask, request
from flask_restful import reqparse, abort, Resource, Api
import time

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return "BlackBeans API"

# Accounts

accounts = [
    {"id": 1, "name": "Bank of Saint Denis"},
    {"id": 2, "name": "Banco do Brasil"}
]

def findAccount(id):
    for account in accounts:
        if account["id"] == id:
            return account

class AccountList(Resource):
    def get(self):
        time.sleep(1)
        return accounts

api.add_resource(AccountList, "/account")

class Account(Resource):
    def get(self, id):
        return findAccount(id)

    def put(self, id):
        account = request.json
        accounts.append(account)
        return findAccount(id)

api.add_resource(Account, "/account/<int:id>")

# Categories

categories = [
    {"id": 1, "name": "Combustível"}
]

def findCategory(id):
    for category in categories:
        if category["id"] == id:
            return category

class CategoryList(Resource):
    def get(self):
        time.sleep(1)
        return categories

api.add_resource(CategoryList, "/category")

class Category(Resource):
    def get(self, id):
        return findCategory(id)

    def put(self, id):
        category = request.json
        accounts.append(account)
        return findCategory(id)

api.add_resource(Category, "/category/<int:id>")

# Beans

beans = [
    {"id": 1, "name": "Posto da Lagoa", "accountID": 1, "categoryID": 1, "value": 100.0, "isCredit": False},
    {"id": 2, "name": "Hiper Select Rio Tavares", "accountID": 1, "categoryID": 1, "value": 119.0, "isCredit": False}
]

def findBean(id):
    for bean in beans:
        if bean["id"] == id:
            return bean

class BeanList(Resource):
    def get(self):
        time.sleep(1)
        return beans

api.add_resource(BeanList, "/bean")

class Bean(Resource):
    def get(self, id):
        return findBean(id)

    def put(self, id):
        bean = request.json
        beans.append(bean)
        return findBean(id)

api.add_resource(Bean, "/bean/<int:id>")

if __name__ == "__main__":
    app.run(debug=False)
