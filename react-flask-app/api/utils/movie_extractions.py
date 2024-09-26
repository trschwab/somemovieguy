import json

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_page(url):
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def gen_film_url(a_str):
    return f"https://letterboxd.com/film/{'/'.join(a_str.split('/')[2:])}"

def get_a_movie_info(url: str) -> pd.DataFrame:
    '''
    Takes in a movie URL like "https://letterboxd.com/film/goon/"
    Returns the DataFrame of the movie's info.
    '''
    url = gen_film_url(url)
    soup = get_page(url)
    
    # Find the JSON-LD script tag containing movie info
    script_tag = soup.find("script", type="application/ld+json")
    if script_tag:
        try:
            movie_data = json.loads(script_tag.string)
            movie_df = pd.json_normalize(movie_data)

            # Filter for the fields you need
            post_df = movie_df[["image", "director", "dateModified", "productionCompany", "releasedEvent", "url",
                                "actor", "dateCreated", "name", "aggregateRating.reviewCount",
                                "aggregateRating.ratingValue", "aggregateRating.ratingCount"]]
            
            # Rename columns
            post_df = post_df.rename(columns={
                "aggregateRating.reviewCount": "reviewCount",
                "aggregateRating.ratingValue": "ratingValue",
                "aggregateRating.ratingCount": "ratingCount"
            })
            
            return post_df
        except json.JSONDecodeError:
            print(f"Error decoding JSON for movie: {url}")
            return pd.DataFrame()  # Return empty DataFrame if parsing fails
    else:
        print(f"No JSON-LD data found for movie: {url}")
        return pd.DataFrame()  # Return empty DataFrame if no script tag is found
