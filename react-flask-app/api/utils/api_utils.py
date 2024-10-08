# utils/update_user_data.py
from utils.table_definitions import UserDiary, Movie
from utils.movie_extractions import get_a_movie_info
from sqlalchemy import and_
from config import LETTERBOXD_BASE_URL
from utils.table_definitions import Movie, UserDiary, db


def update_diary_entries(user_id, user_data_df):
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

        if row['film_link']:
            try:
                url = f"{LETTERBOXD_BASE_URL}{'/'.join(row['film_link'].split('/')[2:])}"
                movie_info_df = get_a_movie_info(url, row['film'])

                if movie_info_df is not None:
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
