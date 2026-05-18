from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ---------------- USER TABLE ----------------
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(20))

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    district = db.Column(db.String(100))

    sector = db.Column(db.String(100))

    cell = db.Column(db.String(100))

    role = db.Column(db.String(20), default="user")


# ---------------- DUSTBIN TABLE ----------------
class Dustbin(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    serial_number = db.Column(db.String(50), unique=True)

    location_name = db.Column(db.String(100))

    district = db.Column(db.String(100))

    sector = db.Column(db.String(100))

    cell = db.Column(db.String(100))

    address = db.Column(db.String(200))

    status = db.Column(db.String(20), default="NOT_FULL")