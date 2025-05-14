import json
import os
from istorage import IStorage

class StorageJson(IStorage):
	"""JSON file-based storage implementation of IStorage interface."""

	def __init__(self, file_path):
		"""Initialize storage with the path to the JSON file."""

		self.file_path = file_path
		...

	def _load(self):
		"""Load movies data from JSON file or return empty dict if not found."""
		if not os.path.exists(self.file_path):
			return {}
		with open(self.file_path, 'r', encoding='utf-8') as f:
			return json.load(f)

	def _save(self, movies):
		"""Save movies data to JSON file."""
		with open(self.file_path, 'w', encoding='utf-8') as f:
			json.dump(movies, f, indent=4, ensure_ascii=False)

	def list_movies(self):
		"""Return all movies as a dictionary."""
		return self._load()

	def add_movie(self, title, year, rating, poster):
		"""Add a new movie entry to storage."""
		movies = self._load()
		movies[title] = {"year": year, "rating": rating, "poster": poster}
		self._save(movies)

	def delete_movie(self, title):
		"""Delete a movie by its title."""
		movies = self._load()
		if title not in movies:
			raise KeyError(f"Movie '{title}' does not exist.")
		del movies[title]
		self._save(movies)

	def update_movie(self, title, rating):
		"""Update the rating of an existing movie."""
		movies = self._load()
		if title not in movies:
			raise KeyError(f"Movie '{title}' does not exist.")
		movies[title]["rating"] = rating
		self._save(movies)