import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.get_stats import get_top_rated_movies, get_combined_user_diary_and_movies, get_user_stats_str
from utils.table_definitions import db, migrate, UserDiary, User, Movie
from utils.lbox_extraction import is_valid_username, get_user_data
from utils.movie_extractions import get_a_movie_info
from sqlalchemy import and_

import pandas as pd

app = Flask(__name__, static_folder="../build", static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Initialize SQLAlchemy and Alembic Migrations
db.init_app(app)
migrate.init_app(app, db)


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

# Run the cleanup function during server initialization or periodically
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

    # Check if username is valid
    if not username:
        return jsonify({'message': 'Username is required!'}), 400

    # Check for existing username
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        user_data_df = get_user_data(username)
        # Update or add diary entries to the database
        for index, row in user_data_df.iterrows():
            # Check for existing diary entry with the same user_id and other key attributes
            existing_entry = UserDiary.query.filter_by(
                user_id=existing_user.id,
                day=row['day'],
                month=row['month'],
                year=row['year'],
                film=row['film']
            ).first()

            if existing_entry is None:
                # If no existing entry is found, add it
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

            # Fetch movie info if film_link exists
            if row['film_link']:
                try:
                    url = f"https://www.letterboxd.com/{'/'.join(row['film_link'].split('/')[2:])}"
                    movie_info_df = get_a_movie_info(url)
                    if movie_info_df is not None:
                        # Create a new Movie object and add to the database
                        existing_movie = Movie.query.filter_by(url=movie_info_df['url'][0]).first()
                        if not existing_movie:
                            new_movie = Movie(
                                name=movie_info_df['name'][0],
                                director=movie_info_df['director'][0],
                                rating_value=movie_info_df['ratingValue'][0],
                                released_event=movie_info_df['releasedEvent'][0],
                                url=movie_info_df['url'][0],
                                image=movie_info_df['image'][0]
                            )
                            db.session.add(new_movie)
                            db.session.commit()
                except Exception as e:
                    print(f"Failed to fetch movie info for {url}: {e}")

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

    for index, row in user_data_df.iterrows():
        # Check for existing diary entry with the same user_id and other key attributes
        existing_entry = UserDiary.query.filter_by(
            user_id=existing_user.id,
            day=row['day'],
            month=row['month'],
            year=row['year'],
            film=row['film']
        ).first()

        if existing_entry is None:
            # If no existing entry is found, add it
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

        # Fetch movie info if film_link exists
        if row['film_link']:
            try:
                url = f"https://www.letterboxd.com/{'/'.join(row['film_link'].split('/')[2:])}"
                movie_info_df = get_a_movie_info(url)
                if movie_info_df is not None:
                    # Create a new Movie object and add to the database
                    existing_movie = Movie.query.filter_by(url=movie_info_df['url'][0]).first()
                    if not existing_movie:  
                        new_movie = Movie(
                            name=movie_info_df['name'][0],
                            director=movie_info_df['director'][0],
                            rating_value=movie_info_df['ratingValue'][0],
                            released_event=movie_info_df['releasedEvent'][0],
                            url=movie_info_df['url'][0],
                            image=movie_info_df['image'][0]
                        )
                        db.session.add(new_movie)
                        db.session.commit()
            except Exception as e:
                print(f"Failed to fetch movie info for {url}: {e}")

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
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found!'}), 404

    diary_entries = UserDiary.query.filter_by(user_id=user.id).all()

    if not diary_entries:
        return jsonify({'message': 'No diary entries found for this user.'}), 404

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

    top_movies = get_top_rated_movies(diary_data)
    top_movies_data = top_movies.to_dict(orient='records')

    return jsonify({
        'username': username,
        'diary_entries': diary_data.to_dict(orient='records'),
        'top_movies': top_movies_data
    }), 200

@app.route('/api/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

# New route to fetch movies from the Movie table
@app.route('/api/movies/', methods=['GET'])
def get_movies():
    movies = Movie.query.all()

    if not movies:
        return jsonify({'message': 'No movies found!'}), 404

    # Convert movie data into JSON format
    movie_data = [{
        'name': movie.name,
        'director': movie.director,
        'rating_value': movie.rating_value,
        'released_event': movie.released_event,
        'url': movie.url,
        'image': movie.image
    } for movie in movies]

    return jsonify({'movies': movie_data}), 200

@app.route('/api/user_diary_combined/<username>/', methods=['GET'])
def get_combined_user_diary(username):
    combined_df = get_combined_user_diary_and_movies(username)
    
    if combined_df is None:
        return jsonify({'message': "error"}), 404

    combined_data = combined_df.to_dict(orient='records')
    return jsonify({'combined_data': combined_data}), 200


@app.route('/api/user_stats_string/<username>/', methods=['GET'])
def get_stats_str(username):
    return_string = get_user_stats_str(username)
    
    if return_string is None:
        return jsonify({'message': "No string returned"}), 404

    # Replace newlines with <br />
    return_string = return_string.replace('\n', '<br />')

    return jsonify({'return_string': return_string}), 200






if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
