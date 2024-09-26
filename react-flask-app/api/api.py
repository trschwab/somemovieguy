import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.get_stats import get_top_rated_movies
from utils.table_definitions import db, migrate, UserDiary, User, Movie
from utils.lbox_extraction import is_valid_username, get_user_data
from utils.movie_extractions import get_a_movie_info

import pandas as pd

app = Flask(__name__, static_folder="../build", static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Initialize SQLAlchemy and Alembic Migrations
db.init_app(app)
migrate.init_app(app, db)

def save_movie_info(url: str):
    url = f"https://letterboxd.com/{'/'.join(url.split('/')[2:])}"
    movie_df = get_a_movie_info(url)
    
    # Prepare data for insertion into the database
    movie_data = {
        "image": movie_df["image"].values[0],
        "director": movie_df["director"].values[0],
        "date_modified": movie_df["dateModified"].values[0],
        "production_company": movie_df["productionCompany"].values[0],
        "released_event": movie_df["releasedEvent"].values[0],
        "url": movie_df["url"].values[0],
        "actors": movie_df["actors"].values[0],
        "date_created": movie_df["dateCreated"].values[0],
        "name": movie_df["name"].values[0],
        "review_count": movie_df["reviewCount"].values[0] or 0,  # Default to 0 if None
        "rating_value": movie_df["ratingValue"].values[0] or 0.0,  # Default to 0.0 if None
        "rating_count": movie_df["ratingCount"].values[0] or 0  # Default to 0 if None
    }

    # Convert `None` values to suitable defaults (if needed)
    for key, value in movie_data.items():
        if value is None:
            if "count" in key:
                movie_data[key] = 0
            elif "rating" in key:
                movie_data[key] = 0.0

    try:
        # Save the movie data to the database
        new_movie = Movie(**movie_data)
        db.session.add(new_movie)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Movie insertion fails, likely movie already exists. Error: {e}")




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

            # Fetch movie info using the film_link and save it in the Movie table
            if row.get('film_link'):
                save_movie_info(row['film_link'])  # Call function to save movie info

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

        # Fetch movie info using the film_link and save it in the Movie table
        if row.get('film_link'):
            save_movie_info(row['film_link'])  # Call function to save movie info

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
