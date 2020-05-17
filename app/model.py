from app import db


class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation = db.Column(db.Float)
    update = db.Column(db.Float)
    isActive = db.Column(db.Boolean)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "creation": self.creation,
            "update": self.update,
            "isActive": self.isActive
        }


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation = db.Column(db.Integer)
    update = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "creation": self.creation,
            "update": self.update
        }
