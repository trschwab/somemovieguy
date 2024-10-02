import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
from utils.table_definitions import Movie


def get_page(url):
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def gen_film_url(a_str):
    return f"https://letterboxd.com/film/{'/'.join(a_str.split('/')[2:])}"


def get_a_movie_info(url: str, film: str) -> pd.DataFrame:
    '''
    Takes in a movie URL like "https://letterboxd.com/film/goon/"
    Returns the DataFrame of the movie's info.
    '''
    # Retrieve the Movie DB
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

    if film in movie_data["name"].unique():
        print(f"{film} found in movie_data, skipping")
        return

    soup = get_page(url)
    i = 0
    begin = 0
    end = 0
    for item in str(soup).split('\n'):
        if ("* <![CDATA[ */" in item):
            begin = i
        if ("/* ]]> */" in item):
            end = i + 1
        i += 1

    info_list = [str(soup).split('\n')[begin:end], url]
    if info_list and len(info_list[0]) > 1:
        movie_df = pd.json_normalize(json.loads(info_list[0][1]))
    else:
        # Handle the case where the structure isn't as expected
        print("Unexpected info_list structure:", info_list)
        return None


    movie_df = pd.json_normalize(json.loads(info_list[0][1]))

    # Filter for the fields you need, setting missing columns to empty strings
    columns_needed = ["image", "director", "dateModified", "productionCompany", "releasedEvent", "url",
                      "actors", "dateCreated", "name", "aggregateRating.reviewCount",
                      "aggregateRating.ratingValue", "aggregateRating.ratingCount"]
    
    for column in columns_needed:
        if column not in movie_df:
            movie_df[column] = None  # Fill missing columns with None

    # Filter and rename columns
    post_df = movie_df[columns_needed].rename(columns={
        "aggregateRating.reviewCount": "reviewCount",
        "aggregateRating.ratingValue": "ratingValue",
        "aggregateRating.ratingCount": "ratingCount"
    })

    # Cast all columns to string to avoid type issues
    post_df = post_df.astype(str)

    # Replace 'None' or 'nan' strings with default values
    post_df = post_df.replace({"None": None, "nan": None})  # None in Python is converted to NULL in SQL

    return post_df
