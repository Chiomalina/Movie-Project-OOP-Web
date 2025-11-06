"""
Interface CRUD
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class IStorage(ABC):
	""" Abstract storage interface exposing CRUD operations for movies."""

	@abstractmethod
	def list_movies(self) -> Dict[str, Dict[str, Any]]:
		"""
        Return the entire movies dictionary, e.g.:
        {
          "Titanic": {"year": "1997", "rating": 7.9, "poster": "https://..."},
          ...
        }
        """
		pass

	@abstractmethod
	def add_movie(self, title: str, year: str, rating: float | None, poster: str | None) -> None:
		"""
        Persist a movie record. No input validation or user interaction here.
        The caller (CLI/service) is responsible for sanitizing/typing.
        """
		pass

	@abstractmethod
	def delete_movie(self, title: str) -> None:
		"""
	    Remove a movie by exact title key, if present.
	    """
		pass

	@abstractmethod
	def update_movie(self, title: str, rating: float | None) -> None:
		"""
	    Update only the rating for an existing movie, if present.
	    """
		pass