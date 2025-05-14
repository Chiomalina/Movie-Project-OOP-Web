from abc import ABC, abstractmethod


class IStorage(ABC):
	"""Interface for movie storage implementations."""

	@abstractmethod
	def list_movies(self):
		""" Return a dictionary of all movies"""
		pass

	@abstractmethod
	def add_movie(self, title, year, rating, poster):
		""" Add a movie with title, release year, rating, and poster info."""
		pass

	@abstractmethod
	def delete_movie(self, title):
		""" Remove a movie by its title."""
		pass

	@abstractmethod
	def update_movie(self, title, rating):
		"""Update the rating of an existing movie."""
		pass
