from app import db
from sqlalchemy import select, func


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    email = db.Column(db.String(200))
    token = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def serialize(self):
        return {
            "name": self.name,
            "email": self.email,
            "token": self.token
        }


class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    color = db.Column(db.String(20))
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    is_active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def sum(self):
        query = select(func.sum(Bean.value))\
            .filter(Bean.account_id == self.id)
        res = db.session.execute(query).all()
        res = res[0][0]
        if (res == None):
            res = 0
        return res

    def serialize(self):
        return {
            "id": self.id,
            "color": self.color,
            "name": self.name,
            "created": self.creation,
            "updated": self.update,
            "isActive": self.is_active,
            "total": self.sum()
        }


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    is_active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "createdTime": self.creation,
            "lastSavedTime": self.update,
            "isActive": self.is_active
        }


class Bean(db.Model):
    __tablename__ = "beans"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    is_active = db.Column(db.Boolean)
    value = db.Column(db.Float)
    is_credit = db.Column(db.Boolean)
    effectivation = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "createdTime": self.creation,
            "lastSavedTime": self.update,
            "isActive": self.isActive,
            "value": self.value,
            "isCredit": self.isCredit,
            "effectivationTime": self.effectivation,
            "accountID": self.account_id,
            "categoryID": self.category_id
        }
