from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from enum import Enum


class Role(Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    ANALYST = "Analyst"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.Enum(Role))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Status(Enum):
    PENDING = "Pending"
    IN_REVIEW = "In review"
    CLOSED = "Closed"


class Group(Enum):
    CUSTOMER_1 = "Customer 1"
    CUSTOMER_2 = "Customer 2"
    CUSTOMER_3 = "Customer 3"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status), default=Status.PENDING)
    group = db.Column(db.Enum(Group))
    note = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
