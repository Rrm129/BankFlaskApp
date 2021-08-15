from . import db
from flask_login import UserMixin
from sqlalchemy import func
import random


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    full_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    account_number = db.Column(db.Integer(), unique=True, default=0)
    transactions = db.relationship('Transaction')
    balance = db.Column(db.Integer, default=0)

    def getBalance(self):
        form_balance = "{:,}".format(self.balance)
        return form_balance

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(10))
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"Transaction('{self.amount}','{self.date}')"

    def getDate(self):
        formatted_date = self.date.strftime('%B %d, %Y')
        return formatted_date
