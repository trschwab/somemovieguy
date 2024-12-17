from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

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

class UserWatchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    film_id = db.Column(db.String(255), nullable=False)
    film_slug = db.Column(db.String(255), nullable=False)
    film_url = db.Column(db.String(255), nullable=False)
    poster_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', backref=db.backref('watchlist_entries', lazy=True))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=True)
    director = db.Column(db.String(255), nullable=True)
    date_modified = db.Column(db.String(50), nullable=True)
    production_company = db.Column(db.String(255), nullable=True)
    released_event = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=False, unique=True)
    actors = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    review_count = db.Column(db.Integer, nullable=True)
    rating_value = db.Column(db.Float, nullable=True)
    rating_count = db.Column(db.Integer, nullable=True)
