import pandas as pd

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


# def get_deviation(joined_table):
#     joined_table = joined_table[joined_table["year"] == "2023"]
#     mapping = {'×': 0,
#                "× ★★★★½": 9,
#                "× ★★½": 5,
#                "× ★★★★": 8,
#                "× ★★★": 6,
#                "× ★★★½": 7
#                }
#     joined_table['numeric_rating'] = joined_table.rating.map(mapping)
#     joined_table = joined_table[joined_table["numeric_rating"] != 0]
#     joined_table["ratingValue"] = joined_table["ratingValue"].astype('float64')
#     joined_table["deviation"] = abs(joined_table["numeric_rating"] - (joined_table["ratingValue"]*2))
#     deviation = joined_table[joined_table["deviation"] >= 2.5]
#     return deviation[["film", "ratingValue", "numeric_rating", "deviation"]]


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