import pandas as pd
import ast

import pandas as pd
from utils.table_definitions import db, UserDiary, Movie, User
import os

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from PIL import Image, ImageEnhance
from io import BytesIO
import logging
import requests
from io import BytesIO
from PIL import Image
from flask import Response
import io

STAR_MAPPING = {
    '×': 0, '× ½': 1, '× ★': 2, '× ★½': 3, '× ★★': 4,
    '× ★★½': 5, '× ★★★': 6, '× ★★★½': 7, '× ★★★★': 8,
    '× ★★★★½': 9, '× ★★★★★': 10
}


def get_topster_helper(username):
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

    diary_data['numeric_rating'] = diary_data.rating.map(STAR_MAPPING)

    top_unique_films = diary_data.sort_values(by='numeric_rating', ascending=False).drop_duplicates('film').nlargest(25, 'numeric_rating')

    # This is randomization
    # Group by 'numeric_rating', shuffle within each group, and concatenate
    top_unique_films_randomized = top_unique_films.groupby('numeric_rating').apply(lambda x: x.sample(frac=1)).reset_index(drop=True)

    # Sort the final result by 'numeric_rating' in descending order
    top_unique_films_randomized = top_unique_films_randomized.sort_values(by='numeric_rating', ascending=False)

    top_unique_films = top_unique_films_randomized
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
    combined_df = pd.merge(top_unique_films, movie_data, left_on='film', right_on='name', how='left')
    combined_df.fillna('', inplace=True)

    image_paths = combined_df["image"].unique()

    # Create a directory to store downloaded images
    os.makedirs('downloaded_images', exist_ok=True)

    # Download the images from the URLs and save them individually
    images = []
    for i, url in enumerate(image_paths):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                images.append(img)
            else:
                raise Exception(f"Failed to fetch image from {url}")
        except Exception as e:
            print(f"Error: {e}")
            # Add a blank white image if any error occurs
            blank_img = Image.new('RGB', (500, 500), color='white')
            images.append(blank_img)

    # # Ensure we have all 25 images
    # if len(images) < 25:
    #     raise ValueError("Not all images could be downloaded successfully")

    # Determine the size of individual images
    img_width, img_height = images[0].size

    # Set the size for the resulting grid
    grid_width = img_width * 5
    grid_height = img_height * 5

    # Create a blank image with a white background
    grid_image = Image.new('RGB', (grid_width, grid_height), color='white')

    # Paste each image into the grid
    for i, image in enumerate(images):
        x_offset = (i % 5) * img_width
        y_offset = (i // 5) * img_height
        grid_image.paste(image, (x_offset, y_offset))

    # Create a BytesIO object to hold the image data
    img_byte_array = io.BytesIO()

    # Save the resulting grid image to the BytesIO object
    grid_image.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)  # Move the cursor to the beginning of the BytesIO object

    return img_byte_array.getvalue()  # Return the binary data
