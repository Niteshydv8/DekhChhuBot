# utils.py
from movie_data import movies
import random

def search_movie_by_name(name):
    name = name.lower()
    return [m for m in movies if name in m['clean_title'].lower() or name in m['title'].lower()]

def search_movie_by_code(code):
    return next((m for m in movies if m['code'].lower() == code.lower()), None)

def get_random_movie():
    return random.choice(movies)
