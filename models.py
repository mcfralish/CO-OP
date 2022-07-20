from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    uid = db.Column(db.String(120), unique=True, nullable=False)
    pw = db.Column(db.String(120), nullable=False)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    icon = db.Column(db.String(120), nullable=False)


class Coops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    link = db.Column(db.String(120), nullable=False)


# class Authorized_Users(db.Model):
#     id = db.Column()
