from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    email = db.Column(db.String)
    token = db.Column(db.String)
    password = db.Column(db.String)

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
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    isActive = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "createdTime": self.creation,
            "lastSavedTime": self.update,
            "isActive": self.isActive
        }


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    isActive = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "createdTime": self.creation,
            "lastSavedTime": self.update,
            "isActive": self.isActive
        }


class Bean(db.Model):
    __tablename__ = "beans"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    isActive = db.Column(db.Boolean)
    value = db.Column(db.Float)
    isCredit = db.Column(db.Boolean)
    effectivation = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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
