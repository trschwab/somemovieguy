import requests
import logging
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


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


def get_user_watchlist(a_user):
    '''
    returns a DF of a user's watchlist information

    # TOOD need to be able to handle users that do not exist
    And try catch blocks
    And logging
    '''
    # Get diary URL
    watchlist_url = get_watchlist(a_user)

    # Extract data from each poster
    posters = []
    while watchlist_url:
        print(watchlist_url)
        r = requests.get(watchlist_url)
        soup = BeautifulSoup(r.content, features="lxml")

        # Find all 'li' elements with the class 'poster-container'
        poster_containers = soup.find_all("li", class_="poster-container")
        for poster in poster_containers:
            div = poster.find("div", class_="film-poster")
            if div:
                film_id = div.get("data-film-id", "")
                film_slug = div.get("data-film-slug", "")
                film_url = div.get("data-target-link", "")
                poster_url = div.get("data-poster-url", "")
                title = div.find("img").get("alt", "")
                
                posters.append({
                    "film_id": film_id,
                    "film_slug": film_slug,
                    "film_url": film_url,
                    "poster_url": poster_url,
                    "title": title,
                })

        # Print extracted data
        # for poster in posters:
            # print(poster)

        # Find out if there are any subsequent pages
        older_link = soup.find_all("a", text="Older")

        if older_link:
            new_page = older_link[0]['href']
            watchlist_url = f"{BASE_URL}{new_page}"
        else:
            watchlist_url = False

    # Convert the list of dictionaries into a pandas DataFrame
    watchlist_df = pd.DataFrame(posters)

    return watchlist_df


BASE_URL = "https://letterboxd.com"

def gen_film_url(a_str):
    return f"https://letterboxd.com/film/{a_str[1].split('/')[3]}/"

def get_diary(a_user):
    return f"{BASE_URL}/{a_user}/films/diary/"

def get_watchlist(a_user):
    return f"{BASE_URL}/{a_user}/watchlist/"


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