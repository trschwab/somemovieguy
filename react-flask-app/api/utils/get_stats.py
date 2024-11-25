import pandas as pd
import ast
from utils.table_definitions import db, UserDiary, Movie, User
import json

STAR_MAPPING = {
    '×': 0, '× ½': 1, '× ★': 2, '× ★½': 3, '× ★★': 4,
    '× ★★½': 5, '× ★★★': 6, '× ★★★½': 7, '× ★★★★': 8,
    '× ★★★★½': 9, '× ★★★★★': 10
}

def get_combined_user_diary_and_movies(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, 'User not found!'
    
    diary_entries = UserDiary.query.filter_by(user_id=user.id).all()
    if not diary_entries:
        return None, 'No diary entries found for this user.'

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

    movies = Movie.query.all()
    if not movies:
        return None, 'No movies found!'

    movie_data = pd.DataFrame([{
        'name': movie.name,
        'director': movie.director,
        'rating_value': movie.rating_value,
        'released_event': movie.released_event,
        'url': movie.url,
        'image': movie.image
    } for movie in movies])

    combined_df = pd.merge(diary_data, movie_data, left_on='film', right_on='name', how='left')
    combined_df.fillna('', inplace=True)

    return combined_df


def get_user_stats_str(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, 'User not found!'
    
    diary_entries = UserDiary.query.filter_by(user_id=user.id).all()
    if not diary_entries:
        return None, 'No diary entries found for this user.'

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

    movies = Movie.query.all()
    if not movies:
        return None, 'No movies found!'

    movie_data = pd.DataFrame([{
        'name': movie.name,
        'director': movie.director,
        'rating_value': movie.rating_value,
        'released_event': movie.released_event,
        'url': movie.url,
        'image': movie.image
    } for movie in movies])

    diary_data['numeric_rating'] = diary_data.rating.map(STAR_MAPPING)

    combined_df = pd.merge(diary_data, movie_data, left_on='film', right_on='name', how='left')
    combined_df.fillna('', inplace=True)

    # Create a json string
    stats_data = {"username": {"data": username, "description": "Data for user"}}

    try:
        yr_count = len(diary_data[diary_data["year"] == "2024"])
        stats_data["2024_watch"] = {"data": yr_count, "description": "Movies watched in 2024"}
    except Exception as e:
        print(e)

    try:
        avg = get_average(diary_data)
        stats_data["avg_rating"] = {"data": f"{avg:.2f}", "description": "Average movie rating"}
    except Exception as e:
        print(e)

    try:
        dev = get_std_dev(diary_data)
        stats_data["std_dev"] = {"data": f"{dev:.2f}", "description": "Rating standard deviation"}
    except Exception as e:
        print(e)

    try:
        top_directors = get_top_director(combined_df)
        stats_data["top_directors"] = {"data": top_directors, "description": "Top Directors"}
    except Exception as e:
        print(e)

    try:
        review_count = get_reviews_per_year(diary_data, "2024")
        stats_data["review_count"] = {"data": review_count, "description": "Reviews left in 2024"}
    except Exception as e:
        print(e)

    try:
        hot_takes_str = get_rating_deviations(combined_df)
        stats_data["hot_takes"] = {"data": hot_takes_str, "description": "Hot Takes (ratings >3 stars from average)"}
    except Exception as e:
        print(e)

    json_string = json.dumps(stats_data)

    return json_string



def get_reviews_per_year(df, year="2024"):
    return len(df[(df["review_link"].notna()) & (df["review_link"] != "") & (df["year"] == year)])


def get_top_director(combined_df):
    directors = combined_df["director"]
    director_list = list(directors)
    director_set = []

    for element in director_list:
        try:
            director_set += ast.literal_eval(element)
        except Exception:
            continue

    df = pd.DataFrame.from_dict(director_set)
    actor_stats = df.groupby(["name"]).size().reset_index(name='counts')
    top_5 = actor_stats.sort_values("counts", ascending=False).head(5)
    top_5 = top_5.to_dict(orient="records")

    return top_5


def get_top_rated_movies(df, top_n=20):
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['rating'])
    
    top_movies = df.sort_values(by='rating', ascending=False).head(top_n)
    return top_movies[['film', 'rating']]


def get_rating_deviations(df):
    df = df[df["numeric_rating"] != 0]
    df['numeric_rating'].fillna(0, inplace=True)
    df['numeric_rating'] = pd.to_numeric(df['numeric_rating'], errors='coerce')
    df['rating_value'] = pd.to_numeric(df['rating_value'], errors='coerce')

    df.dropna(subset=['numeric_rating', 'rating_value'], inplace=True)

    deviation_mask = (df['numeric_rating'] - (df['rating_value'] * 2)).abs() > 3
    deviated_df = df[deviation_mask]
    
    result_list = []
    for _, row in deviated_df.iterrows():
        element = {"film": row['film'],
         "user_rating": row['numeric_rating'],
         "movie_rating": row['rating_value'] * 2}
        result_list += [element]

    return result_list


def get_average(user_data):
    user_data = user_data[user_data["numeric_rating"] != 0]
    return user_data['numeric_rating'].mean()


def get_std_dev(user_data):
    user_data = user_data[user_data["numeric_rating"] != 0]
    return user_data['numeric_rating'].std()
