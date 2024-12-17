import time
import random
import pandas as pd
from flask import Flask, Response, jsonify, request
import json
from flask_cors import CORS
from sqlalchemy import and_
from utils.api_utils import update_diary_entries
from utils.get_stats import (get_combined_user_diary_and_movies,
                             get_top_rated_movies, get_user_stats_str)
from utils.get_topster import get_topster_helper
from utils.lbox_extraction import get_user_data, is_valid_username
from utils.movie_extractions import get_a_movie_info
from utils.table_definitions import Movie, User, UserDiary, UserWatchlist, db, migrate

app = Flask(__name__, static_folder="../build", static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

# Initialize SQLAlchemy and Alembic Migrations
db.init_app(app)
migrate.init_app(app, db)

# Create all tables if they don't exist
with app.app_context():
    db.create_all()

def remove_duplicates():
    users = User.query.all()
    for user in users:
        entries = UserDiary.query.filter_by(user_id=user.id).all()
        unique_entries = {}
        duplicates = []

        for entry in entries:
            # Create a unique key based on the entry's fields to identify duplicates
            key = (entry.user_id, entry.day, entry.month, entry.year, entry.film)

            if key not in unique_entries:
                unique_entries[key] = entry
            else:
                duplicates.append(entry)

        # Remove duplicate entries from the database
        for duplicate in duplicates:
            db.session.delete(duplicate)

    db.session.commit()

with app.app_context():
    remove_duplicates()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/time/')
def get_current_time():
    return {'time': str(int(time.time()))}

@app.route('/api/users/', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')

    if not is_valid_username(username):
        return jsonify({'message': 'Username is invalid on Letterboxd!'}), 400

    if not username:
        return jsonify({'message': 'Username is required!'}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        user_data_df = get_user_data(username)
        update_diary_entries(existing_user.id, user_data_df)
        return jsonify({
            'message': 'Username processed; diary entries updated!',
            'user_data': user_data_df.to_dict(orient='records')
        }), 200
    else:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()

        user_data_df = get_user_data(username)
        update_diary_entries(new_user.id, user_data_df)

        return jsonify({
            'message': 'User added successfully!',
            'user_data': user_data_df.to_dict(orient='records')
        }), 201

@app.route('/api/user_watchlist/<username>/', methods=['POST'])
def populate_user_watchlist(username):
    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    # Call the get_user_watchlist function
    from utils.lbox_extraction import get_user_watchlist
    try:
        watchlist_df = get_user_watchlist(username)
    except Exception as e:
        return jsonify({'message': f"Error fetching watchlist: {str(e)}"}), 500

    if watchlist_df.empty:
        return jsonify({'message': 'No watchlist found for this user.'}), 404

    # Add entries to the UserWatchlist table
    added_count = 0
    for _, row in watchlist_df.iterrows():
        # Check for duplicates
        existing_entry = UserWatchlist.query.filter_by(
            user_id=user.id,
            film_id=row['film_id']
        ).first()
        if not existing_entry:
            new_entry = UserWatchlist(
                user_id=user.id,
                film_id=row['film_id'],
                film_slug=row['film_slug'],
                film_url=row['film_url'],
                poster_url=row['poster_url'],
                title=row['title']
            )
            db.session.add(new_entry)
            added_count += 1

    db.session.commit()

    # Convert the DataFrame to JSON and return it
    return jsonify({
        'message': f'{added_count} new entries added to the watchlist.',
        'watchlist': watchlist_df.to_dict(orient='records')
    }), 200

@app.route('/api/random_watchlist_movie/<username>/', methods=['GET'])
def get_random_watchlist_movie(username):
    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    # Retrieve the user's watchlist
    watchlist = UserWatchlist.query.filter_by(user_id=user.id).all()

    if not watchlist:
        return jsonify({'message': 'Watchlist is empty!'}), 404

    # Pick a random movie from the watchlist
    random_movie = random.choice(watchlist)

    return jsonify({
        'movie': {
            'title': random_movie.title,
            'film_url': random_movie.film_url,
            'poster_url': random_movie.poster_url
        }
    }), 200

@app.route('/api/movies/', methods=['GET'])
def get_movies():
    movies = Movie.query.all()

    if not movies:
        return jsonify({'message': 'No movies found!'}), 404

    movie_data = [{
        'name': movie.name,
        'director': movie.director,
        'rating_value': movie.rating_value,
        'released_event': movie.released_event,
        'url': movie.url,
        'image': movie.image
    } for movie in movies]

    return jsonify({'movies': movie_data}), 200

@app.route('/api/user_stats_string/<username>/', methods=['GET'])
def get_stats_str(username):
    return_string = json.loads(get_user_stats_str(username))
    
    if return_string is None:
        return jsonify({'message': "No string returned"}), 404

    return jsonify({'return_string': return_string}), 200

@app.route('/api/get_topster/<username>/', methods=['GET'])
def get_topster(username):
    img_data = get_topster_helper(username)
    
    if img_data is None:
        return jsonify({'message': "No image generated"}), 404

    return Response(img_data, mimetype='image/png')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
