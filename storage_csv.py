# storage_csv.py
"""
CSV file-based storage implementation of the IStorage interface.
"""
import csv
import os
from istorage import IStorage


class StorageCsv(IStorage):
    """Stores movie data in a CSV file with columns: title,year,rating,poster."""

    def __init__(self, file_path):
        """Initialize StorageCsv with the path to the CSV file."""
        self.file_path = file_path

    def _load(self):
        """Load movies from CSV into a dict. Returns {} if file doesn't exist."""
        movies = {}
        if not os.path.exists(self.file_path):
            return movies
        with open(self.file_path, mode='r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row['title']
                try:
                    year = int(row['year'])
                except ValueError:
                    year = None
                try:
                    rating = float(row['rating'])
                except ValueError:
                    rating = None
                poster = row.get('poster', '')
                movies[title] = {'year': year, 'rating': rating, 'poster': poster}
        return movies

    def _save(self, movies):
        """Save the movies dict to CSV, overwriting existing file."""
        with open(self.file_path, mode='w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['title', 'year', 'rating', 'poster']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for title, info in movies.items():
                writer.writerow({
                    'title': title,
                    'year': info.get('year', ''),
                    'rating': info.get('rating', ''),
                    'poster': info.get('poster', '')
                })

    def list_movies(self):
        """Return all movies as a dict: {title: {'year':..., 'rating':..., 'poster':...}}"""
        return self._load()

    def add_movie(self, title, year, rating, poster):
        """Add a new movie record to the CSV."""
        movies = self._load()
        movies[title] = {'year': year, 'rating': rating, 'poster': poster}
        self._save(movies)

    def delete_movie(self, title):
        """Delete a movie by title; raises KeyError if not found."""
        movies = self._load()
        if title not in movies:
            raise KeyError(f"Movie '{title}' does not exist.")
        del movies[title]
        self._save(movies)

    def update_movie(self, title, rating):
        """Update the rating of an existing movie; raises KeyError if not found."""
        movies = self._load()
        if title not in movies:
            raise KeyError(f"Movie '{title}' does not exist.")
        movies[title]['rating'] = rating
        self._save(movies)
