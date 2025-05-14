import json
import os

# Path to the JSON file for persistent storage
DATA_FILE = "data.json"

def get_movies():
    """
    Reads and returns the entire movies database from the JSON file.
    If the file doesn't exist yet, returns an empty dict.
    """
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_movies(movies):
    """
    Overwrites the JSON file with the provided movies dictionary.
    """
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

def add_movie(title, year, rating):
    """
    Adds a new movie entry to the JSON database.
    Raises ValueError if the movie already exists.
    """
    movies = get_movies()
    if title in movies:
        raise ValueError(f"Movie '{title}' already exists.")
    movies[title] = {
        "year":   year,
        "rating": rating
    }
    save_movies(movies)

def delete_movie(title):
    """
    Removes a movie from the JSON database.
    Raises KeyError if the movie does not exist.
    """
    movies = get_movies()
    if title not in movies:
        raise KeyError(f"Movie '{title}' does not exist.")
    del movies[title]
    save_movies(movies)

def update_movie(title, new_rating):
    """
    Updates the rating of an existing movie in the JSON database.
    Raises KeyError if the movie does not exist.
    """
    movies = get_movies()
    if title not in movies:
        raise KeyError(f"Movie '{title}' does not exist.")
    movies[title]["rating"] = new_rating
    save_movies(movies)
