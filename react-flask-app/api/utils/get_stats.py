import pandas as pd
import ast

import pandas as pd
from utils.table_definitions import db, UserDiary, Movie, User

def get_combined_user_diary_and_movies(username):
    # Get user by username
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, 'User not found!'
    
    # Query user diary entries
    diary_entries = UserDiary.query.filter_by(user_id=user.id).all()
    if not diary_entries:
        return None, 'No diary entries found for this user.'

    # Convert user diary entries to DataFrame
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

    # Query all movies from the Movie table
    movies = Movie.query.all()
    if not movies:
        return None, 'No movies found!'

    # Convert movie entries to DataFrame
    movie_data = pd.DataFrame([{
        'name': movie.name,
        'director': movie.director,
        'rating_value': movie.rating_value,
        'released_event': movie.released_event,
        'url': movie.url,
        'image': movie.image
    } for movie in movies])

    # Perform the join based on the film name
    combined_df = pd.merge(diary_data, movie_data, left_on='film', right_on='name', how='left')
    combined_df.fillna('', inplace=True)
    return combined_df


def get_user_stats_str(username):
    # Get user by username
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, 'User not found!'
    
    # Query user diary entries
    diary_entries = UserDiary.query.filter_by(user_id=user.id).all()
    if not diary_entries:
        return None, 'No diary entries found for this user.'

    # Convert user diary entries to DataFrame
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

    # Query all movies from the Movie table
    movies = Movie.query.all()
    if not movies:
        return None, 'No movies found!'

    # Convert movie entries to DataFrame
    movie_data = pd.DataFrame([{
        'name': movie.name,
        'director': movie.director,
        'rating_value': movie.rating_value,
        'released_event': movie.released_event,
        'url': movie.url,
        'image': movie.image
    } for movie in movies])

    # Get stats string
    mapping = {
        '×': 0,
        '× ½': 1,
        '× ★': 2,
        '× ★½': 3,
        '× ★★': 4,
        "× ★★½": 5,
        "× ★★★": 6,
        "× ★★★½": 7,
        "× ★★★★": 8,
        "× ★★★★½": 9,
        '× ★★★★★': 10
    }

    diary_data['numeric_rating'] = diary_data.rating.map(mapping)

    # Perform the join based on the film name
    combined_df = pd.merge(diary_data, movie_data, left_on='film', right_on='name', how='left')
    combined_df.fillna('', inplace=True)

    return_string = ""

    # movies watched in 2024
    yr_count = len(diary_data[diary_data["year"] == "2024"])
    
    return_string += f"{username} watched {yr_count} movies in 2024\n"

    # Get average of a user
    avg = get_average(diary_data)
    return_string += f"{username} on average rated movies {avg}\n"

    # Get deviation of a user
    dev = get_std_dev(diary_data)
    return_string += f"{username} had a std deviation in their rating of {dev}\n"
    combined_df.to_csv("combined.csv")

    # Get top director
    dir = get_top_director(combined_df)
    return_string += f"{username} has a top director of \n{dir}\n"

    # Get reviews
    review_count = get_reviews_per_year(diary_data, "2024")
    return_string += f"{username} left {review_count} reviews in 2024\n"

    # Get hot takes
    hot_takes_str = get_rating_deviations(combined_df)
    return_string += f"{username} deviated from mainstream ratings by >3 stars for these movies:\n{hot_takes_str}\n"

    print(return_string)

    return return_string



def get_reviews_per_year(df, year="2024"):
    return len(df[(df["review_link"].notna()) &
                  (df["review_link"] != "") &
                  (df["year"] == year)])

def get_top_director(combined_df):
    directors = combined_df["director"]
    director_list = list(directors)
    director_set = []

    for element in director_list:
        try:
            director_set += ast.literal_eval(element)
        except Exception as e:
            continue
            # print("Error:", e)
            # print("director likely NA type")

    df = pd.DataFrame.from_dict(director_set)
    actor_stats = df.groupby(["name"]).size().reset_index(name='counts')
    top_5 = actor_stats.sort_values("counts", ascending=False).head(5)
    
    # Create a string representation of the top 5 directors
    string_top_5 = top_5.to_string(index=False)
    
    return string_top_5


def get_top_rated_movies(df, top_n=20):
    # Ensure ratings are numeric and filter out entries with no rating
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['rating'])
    
    # Sort movies by rating in descending order and return the top 20
    top_movies = df.sort_values(by='rating', ascending=False).head(top_n)
    
    # Select relevant columns
    return top_movies[['film', 'rating']]


# import ast

# import pandas as pd
# import requests
# import logging

def get_rating_deviations(df):
    df = df[df["numeric_rating"] != 0]
    
    # Replace any unmapped ratings (which result in NaN) with a default value, e.g., 0
    df['numeric_rating'].fillna(0, inplace=True)

    # Convert numeric_rating to a numeric type
    df['numeric_rating'] = pd.to_numeric(df['numeric_rating'], errors='coerce')

    # Ensure rating_value is numeric
    df['rating_value'] = pd.to_numeric(df['rating_value'], errors='coerce')

    # Drop rows where rating_value or numeric_rating is NaN (could not be converted)
    df.dropna(subset=['numeric_rating', 'rating_value'], inplace=True)

    # Calculate the deviation between numeric_rating and rating_value * 2
    deviation_mask = (df['numeric_rating'] - (df['rating_value'] * 2)).abs() > 3

    # Filter the dataframe for deviations greater than 2
    deviated_df = df[deviation_mask]
    
    # Format the results into a string
    result_string = ""
    for _, row in deviated_df.iterrows():
        result_string += f"Film: {row['film']}, Rating: {row['numeric_rating']}, Average Rating: {row['rating_value'] * 2}\n"
    
    return result_string



def get_average(user_data):
    user_data = user_data[user_data["numeric_rating"] != 0]
    return user_data['numeric_rating'].mean()

def get_std_dev(user_data):
    user_data = user_data[user_data["numeric_rating"] != 0]
    return user_data['numeric_rating'].std()


def get_deviation(joined_table):
    joined_table = joined_table[joined_table["year"] == "2023"]
    mapping = {'×': 0,
               "× ★★★★½": 9,
               "× ★★½": 5,
               "× ★★★★": 8,
               "× ★★★": 6,
               "× ★★★½": 7
               }
    joined_table['numeric_rating'] = joined_table.rating.map(mapping)
    joined_table = joined_table[joined_table["numeric_rating"] != 0]
    joined_table["ratingValue"] = joined_table["ratingValue"].astype('float64')
    joined_table["deviation"] = abs(joined_table["numeric_rating"] - (joined_table["ratingValue"]*2))
    deviation = joined_table[joined_table["deviation"] >= 2.5]
    return deviation[["film", "ratingValue", "numeric_rating", "deviation"]]


# # Top production companies?
# def get_production_companies(joined_table):
#     joined_table = joined_table[joined_table["year"] == "2023"]
#     production = joined_table["productionCompany"]
#     production_list = list(production)
#     production_set = []
#     for element in production_list:
#         try:
#             production_set += ast.literal_eval(element)
#         except Exception as e:
#             logging.info(e)
#             logging.info("director likely NA type")
#     df = pd.DataFrame.from_dict(production_set)
#     actor_stats = df.groupby(["name"]).size().reset_index(name='counts')
#     top_10 = actor_stats.sort_values("counts", ascending=False).head(5)
#     return top_10


# # Top actors
# def get_actors(joined_table):
#     joined_table = joined_table[joined_table["year"] == "2023"]
#     actors = joined_table["actors"]
#     actor_list = list(actors)
#     actor_set = []
#     for element in actor_list:
#         try:
#             actor_set += ast.literal_eval(element)
#         except Exception as e:
#             logging.info(e)
#             logging.info("actor likely NA type")
#     df = pd.DataFrame.from_dict(actor_set)
#     actor_stats = df.groupby(["name"]).size().reset_index(name='counts')
#     top_10 = actor_stats.sort_values("counts", ascending=False).head(5)
#     return top_10


# # Top Directors?
# def get_directors(joined_table):
#     joined_table = joined_table[joined_table["year"] == "2023"]
#     directors = joined_table["director"]
#     director_list = list(directors)
#     director_set = []
#     for element in director_list:
#         try:
#             director_set += ast.literal_eval(element)
#         except Exception as e:
#             logging.info(e)
#             logging.info("director likely NA type")
#     df = pd.DataFrame.from_dict(director_set)
#     actor_stats = df.groupby(["name"]).size().reset_index(name='counts')
#     top_10 = actor_stats.sort_values("counts", ascending=False).head(5)
#     return top_10


# # How many movies did the user watch in 2023?
# def get_watch_per_year(df):
#     return len(df[df["year"] == "2023"])


# def get_reviews_per_year(df):
#     return len(df[(df["review_link"] != "None") &
#                   (df["year"] == "2023")])


# def get_average_rating(df):
#     df = df[df["year"] == "2023"]
#     mapping = {'×': 0,
#                '0': 0,
#                '× ½': 1,
#                '× ★': 2,
#                '× ★½': 3,
#                '× ★★': 4,
#                "× ★★½": 5,
#                "× ★★★": 6,
#                "× ★★★½": 7,
#                "× ★★★★": 8,
#                "× ★★★★½": 9,
#                '× ★★★★★': 10
#     }
#     df['numeric_rating'] = df.rating.map(mapping)
#     df = df[df["numeric_rating"] != 0]
#     return df["numeric_rating"].mean()


# def generate_stats_string(user):
#     return_string = ""

#     get_r = requests.get(f"{ROOT}endpoint/movie_table/", auth=('username1', 'password1'))
#     movie_table = pd.DataFrame(get_r.json()).fillna("")

#     get_r = requests.get(f"{ROOT}endpoint/hydrated_data/", auth=('username1', 'password1'))
#     hyd_table = pd.DataFrame(get_r.json()).fillna("")

#     user_info = hyd_table[hyd_table["name"] == user]

#     movie_count = get_watch_per_year(user_info)
#     return_string += f"User watched {movie_count} movies in 2023<br><br>"

#     review_count = get_reviews_per_year(user_info)
#     return_string += f"User reviewed {review_count} of those movies in 2023<br><br>"

#     return_string += f"Only {review_count / movie_count * 100}% of movies watched in 2023 were reviewed<br><br>"

#     average_rating = get_average_rating(user_info)
#     average_rating = average_rating // 0.01 / 100 # int divide to get 2 decimal points
#     return_string += f"On average, you rated movies at {average_rating} in 2023, excluding the 0 star entries<br><br>"

#     try:
#         user_info = user_info.dropna()
#         user_info["film_url"] = user_info.apply(lambda x: f"https://letterboxd.com/{'/'.join(x['film_link'].split('/')[2:4])}/" if x['film_link'] != '' else '', axis=1)

#         join_info = pd.merge(user_info, movie_table, how="left", left_on="film_url", right_on="url")
#     except Exception as e:
#         logging.info("ERROR HERE")
#         logging.info(e)

#     return_string += "User top watched actors were the following:<br><br>"
#     actor_df = get_actors(join_info)
#     actor_dict = actor_df.to_dict('records')
#     for actor in actor_dict:
#         return_string += f"{actor['name']}: {actor['counts']}<br>"
#     return_string += "<br><br>"

#     return_string += "User top watched directors were the following: <br><br>"
#     director_df = get_directors(join_info)
#     director_dict = director_df.to_dict('records')
#     for director in director_dict:
#         return_string += f"{director['name']}: {director['counts']}<br>"
#     return_string += "<br><br>"

#     return_string += "User top watched production companies were the following: <br><br>"
#     prod_df = get_production_companies(join_info)
#     prod_dict = prod_df.to_dict('records')
#     for prod in prod_dict:
#         return_string += f"{prod['name']}: {prod['counts']}<br>"
#     return_string += "<br><br>"

#     return_string += "You deviated from mainstream ratings by greater than 2 and a half stars: <br><br>"
#     deviation_df = get_deviation(join_info)
#     deviation_dict = deviation_df.to_dict('records')
#     for deviation in deviation_dict:
#         return_string += f"{deviation['film']}: You rated {deviation['numeric_rating']} deviating by {deviation['deviation'] // .01 / 100} from the average of {deviation['ratingValue']*2}<br><br>"
#     return_string += "<br><br>"

#     # return return_string
#     return return_string