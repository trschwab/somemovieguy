import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from utils.get_stats import get_top_rated_movies
from utils.table_definitions import db, migrate, UserDiary, User
from utils.lbox_extraction import (is_valid_username, get_user_data)



app = Flask(__name__, static_folder="../build", static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

from flask import g
import sqlite3

def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect('users.db')  # Ensure this matches your database URI
        g.db.row_factory = sqlite3.Row  # This allows you to access columns by name
    return g.db

@app.teardown_appcontext
def close_db_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


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

    # Check if username is valid
    if not username:
        return jsonify({'message': 'Username is required!'}), 400

    # Check for existing username
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        user_data_df = get_user_data(username)
        
        # Update or add diary entries to the database
        for index, row in user_data_df.iterrows():
            diary_entry = UserDiary(
                user_id=existing_user.id,
                day=row['day'],
                month=row['month'],
                year=row['year'],
                film=row['film'],
                released=row.get('released', None),
                rating=row.get('rating', None),
                review_link=row.get('review_link', None),
                film_link=row.get('film_link', None)
            )
            db.session.add(diary_entry)

        db.session.commit()

        # Return the user data along with a success message
        user_data_json = user_data_df.to_dict(orient='records')
        return jsonify({
            'message': 'Username already exists and diary entries updated!',
            'user_data': user_data_json
        }), 200

    # Add new user and save diary entries to the database
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    # Fetch user data and create a DataFrame
    user_data_df = get_user_data(username)

    # Save each diary entry to the UserDiary table
    for index, row in user_data_df.iterrows():
        diary_entry = UserDiary(
            user_id=new_user.id,
            day=row['day'],
            month=row['month'],
            year=row['year'],
            film=row['film'],
            released=row.get('released', None),
            rating=row.get('rating', None),
            review_link=row.get('review_link', None),
            film_link=row.get('film_link', None)
        )
        db.session.add(diary_entry)

    # Commit the new diary entries to the database
    db.session.commit()

    # Return the user data along with a success message
    user_data_json = user_data_df.to_dict(orient='records')
    return jsonify({
        'message': 'User added successfully!',
        'user_data': user_data_json
    }), 201


@app.route('/api/user_diary/<username>/', methods=['GET'])
def get_user_diary(username):
    # Find the user by username
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found!'}), 404

    # Get all diary entries for this user
    diary_entries = UserDiary.query.filter_by(user_id=user.id).all()

    # If no diary entries are found
    if not diary_entries:
        return jsonify({'message': 'No diary entries found for this user.'}), 404

    # Convert diary entries to a DataFrame
    diary_data = pd.DataFrame([{
        'day': entry.day,
        'month': entry.month,
        'year': entry.year,
        'film': entry.film,
        'released': entry.released,
        'rating': entry.rating,
        'review_link': entry.review_link,
        'film_link': entry.film_link
    } for entry in diary_entries])

    # Get top rated movies
    top_movies = get_top_rated_movies(diary_data)

    # Convert top movies to a list of dictionaries
    top_movies_data = top_movies.to_dict(orient='records')

    return jsonify({
        'username': username,
        'diary_entries': diary_data.to_dict(orient='records'),
        'top_movies': top_movies_data
    }), 200


def fetch_user_diary_entries(username):
    conn = get_db_connection()  # Get the database connection
    cursor = conn.cursor()

    # Find the user by username
    user = User.query.filter_by(username=username).first()
    if not user:
        return None  # User not found

    # Fetch diary entries for the specified username
    cursor.execute('SELECT film, rating FROM user_diary WHERE user_id = ?', (user.id,))
    entries = cursor.fetchall()

    # Convert the fetched entries to a list of dictionaries
    return [{'film': entry['film'], 'rating': entry['rating']} for entry in entries]



@app.route('/api/user_stats/<username>/', methods=['GET'])
def get_user_stats(username):
    # Assuming you have a function to fetch user diary entries based on username
    user_diary_entries = fetch_user_diary_entries(username)  # Replace with your actual data fetching method

    # If user diary entries are not found, handle it
    if user_diary_entries is None:
        return jsonify({'message': 'User not found or no diary entries available.'}), 404

    # Sort entries by rating and select the top 20
    top_movies = sorted(user_diary_entries, key=lambda x: x['rating'], reverse=True)[:20]

    # Prepare the response
    stats = [{'title': movie['film'], 'rating': movie['rating']} for movie in top_movies]

    return jsonify({'top_movies': stats}), 200


@app.route('/api/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
