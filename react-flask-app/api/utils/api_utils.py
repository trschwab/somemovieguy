# utils/update_user_data.py
from utils.table_definitions import UserDiary, Movie
from utils.movie_extractions import get_a_movie_info
from sqlalchemy import and_
from utils.table_definitions import Movie, UserDiary, db
import pandas as pd


LETTERBOXD_BASE_URL = "https://www.letterboxd.com/"

def update_diary_entries(user_id, user_data_df):
    # First, update the user diary entries
    for index, row in user_data_df.iterrows():
        existing_entry = UserDiary.query.filter_by(
            user_id=user_id,
            day=row['day'],
            month=row['month'],
            year=row['year'],
            film=row['film']
        ).first()

        if existing_entry is None:
            diary_entry = UserDiary(
                user_id=user_id,
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

    # Now, check for movies in user_data_df that are not in the Movie table
    # Query all movies from the Movie table
    movie_df = pd.DataFrame([{
        'name': movie.name,
        'url': movie.url  # Assuming the unique identifier is the URL
    } for movie in Movie.query.all()])

    # Left join user_data_df with movie_df on 'film' (or 'film_link' if you're matching URLs)
    combined_df = pd.merge(user_data_df, movie_df, left_on='film', right_on='name', how='left', indicator=True)

    # Filter rows where there was no match in the Movie table ('_merge' == 'left_only')
    missing_movies_df = combined_df[combined_df['_merge'] == 'left_only']
    print(f"Length of movies to add: {len(missing_movies_df)}")

    # Iterate over missing movies and fetch the movie info
    for index, row in missing_movies_df.iterrows():
        if row['film_link']:  # Ensure there's a film link to fetch info
            try:
                
                url = f"{LETTERBOXD_BASE_URL}{'/'.join(row['film_link'].split('/')[2:4])}/"
                print(f"Attempting to add: \n\t{row['film_link']}\n\t{url}")
                movie_info_df = get_a_movie_info(url, row['film'])

                if movie_info_df is not None:
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
