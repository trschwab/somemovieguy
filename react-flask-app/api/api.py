import time
import requests
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

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

def is_valid_username(username):
    '''
    Checks to see if a username exists with letterboxd
    '''
    url = f"https://letterboxd.com/{username}/"
    r = requests.get(url)
    if r.status_code == 200:
        logging.info("Valid username supplied")
        return True
    logging.info("Invalid username supplied")
    return False


def get_user_diary_info(a_user):
    '''
    returns a DF of a user's diary information

    # TOOD need to be able to handle users that do not exist
    '''
    df_list = []
    # Get diary URL
    diary_url = get_diary(a_user)
    while diary_url:
        r = requests.get(diary_url)
        soup = BeautifulSoup(r.content, features="lxml")


        # Extract the table as a df
        table = soup.find_all('table')
        df_list.append(pd.read_html(StringIO(str(table)), extract_links="all")[0])

        # Find out if there are any subsequent pages
        older_link = soup.find_all("a", text="Older")

        if older_link:
            new_page = older_link[0]['href']
            diary_url = f"{BASE_URL}{new_page}"
        else:
            diary_url = False
    return_df = pd.concat(df_list)

    return_df["film_url"] = return_df[('Film', None)].apply(lambda x: gen_film_url(x))

    return return_df

BASE_URL = "https://letterboxd.com"

def gen_film_url(a_str):
    return f"https://letterboxd.com/film/{a_str[1].split('/')[3]}/"

def get_diary(a_user):
    return f"{BASE_URL}/{a_user}/films/diary/"


def get_user_data(user: str) -> pd.DataFrame:
    '''
    Gets a df of user data ready to be posted to our model
    '''
    user_df = get_user_diary_info(user)

    c_names = ["month", "day", "film", "released", "rating", "like", "rewatch", "review", "edityou", "film_url"]  # , "img_url", "small_img_url"]

    for i in range(len(c_names)):
        user_df.rename(columns={ user_df.columns[i]: c_names[i] }, inplace=True)

    # user_df.to_csv("expected.csv")
    # explode tuple values into new cols:

    user_df[["month", "month_none"]] = pd.DataFrame(user_df['month'].tolist(), index=user_df.index)
    user_df[["day", "day_none"]] = pd.DataFrame(user_df['day'].tolist(), index=user_df.index)
    user_df[["film", "film_link"]] = pd.DataFrame(user_df['film'].tolist(), index=user_df.index)
    user_df[["released", "released_none"]] = pd.DataFrame(user_df['released'].tolist(), index=user_df.index)
    user_df[["rating", "rating_none"]] = pd.DataFrame(user_df['rating'].tolist(), index=user_df.index)
    user_df[["review", "review_link"]] = pd.DataFrame(user_df['review'].tolist(), index=user_df.index)

    # Convert to dict for iterative processing.. TODO fix this
    dict_df = user_df.to_dict('records')

    for count, item in enumerate(dict_df):
        if item["month"] == '':
            item["month"] = dict_df[count-1]["month"]

    dated_df = pd.DataFrame(dict_df)
    dated_df[["month", "year"]] = dated_df['month'].str.split(' ', expand=True)

    dated_df["name"] = user

    dated_df = dated_df[[
        "name",
        "day",
        "month",
        "year",
        "film",
        "released",
        "rating",
        "review_link",
        "film_link"]]

    return dated_df

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
        return jsonify({'message': 'Username is invalid on letterboxd!'}), 400

    # Check if username is valid
    if not username:
        return jsonify({'message': 'Username is required!'}), 400

    # Check for existing username
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        user_data_df = get_user_data(username)
        
        # Instead of saving to a CSV, save to the database
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
        return jsonify({'message': 'Username already exists and diary entries updated!'}), 409

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
    return jsonify({'message': 'User added successfully!', 'user_data': user_data_json}), 201


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

    # Convert diary entries to a list of dictionaries
    diary_data = [{
        'day': entry.day,
        'month': entry.month,
        'year': entry.year,
        'film': entry.film,
        'released': entry.released,
        'rating': entry.rating,
        'review_link': entry.review_link,
        'film_link': entry.film_link
    } for entry in diary_entries]

    return jsonify({'username': username, 'diary_entries': diary_data}), 200


@app.route('/api/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
