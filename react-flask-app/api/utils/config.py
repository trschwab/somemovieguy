# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# API URLs
LETTERBOXD_BASE_URL = "https://www.letterboxd.com/"


STAR_MAPPING = {
    '×': 0, '× ½': 1, '× ★': 2, '× ★½': 3, '× ★★': 4,
    '× ★★½': 5, '× ★★★': 6, '× ★★★½': 7, '× ★★★★': 8,
    '× ★★★★½': 9, '× ★★★★★': 10
}