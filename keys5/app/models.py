from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    places_to_visit = db.Column(db.Text)
    overall_rating = db.Column(db.Integer)
    transportation_rating = db.Column(db.Integer)
    safety_rating = db.Column(db.Integer)
    population_rating = db.Column(db.Integer)
    vegetation_rating = db.Column(db.Integer)

    user = db.relationship('User', backref=db.backref('trips', lazy=True))
