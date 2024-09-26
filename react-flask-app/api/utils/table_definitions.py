from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, static_folder="../build", static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserDiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day = db.Column(db.String(10), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    film = db.Column(db.String(255), nullable=False)
    released = db.Column(db.String(20), nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    review_link = db.Column(db.String(255), nullable=True)
    film_link = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref=db.backref('diary_entries', lazy=True))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)