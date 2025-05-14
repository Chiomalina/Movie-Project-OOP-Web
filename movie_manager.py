import requests

# Configuration
OMDB_API_URL = "http://www.omdbapi.com/"
OMDB_API_KEY = "6b07de0b"


class Movie:
	def __init__(self, title: str, year: str, rating: str, poster_url: str):
		self.title = title
		self.year = year
		self.rating = rating
		self.poster_url = poster_url

	def __str__(self):
		return f"{self.title} ({self.year}) - Rating: {self.rating}\nPoster: {self.poster_url}"


class MovieCollection:
	def __init__(self):
		self.movies = []

	def add_movie(self, title: str):
		"""
		Fetch movie data from OMDb by title and add to the collection.
		Raises:
			ValueError: if movie not found in OMDb
			requests.exceptions.RequestException: if the API is unreachable
		"""
		params = {
			't': title,
			'apikey': OMDB_API_KEY
		}
		try:
			response = requests.get(OMDB_API_URL, params=params, timeout=5)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			raise requests.exceptions.RequestException(
				f"Error connecting to OMDb API: {e}"
			)

		data = response.json()
		if data.get('Response') == 'False':
			# Movie not found
			raise ValueError(f"Movie '{title}' not found in OMDb.")

		# Extract fields
		movie_title = data.get('Title', 'N/A')
		movie_year = data.get('Year', 'N/A')
		movie_rating = data.get('imdbRating', 'N/A')
		poster_url = data.get('Poster', '')

		movie = Movie(
			title=movie_title,
			year=movie_year,
			rating=movie_rating,
			poster_url=poster_url
		)
		self.movies.append(movie)
		print(f"Added movie: {movie_title} ({movie_year})")

	def delete_movie(self, title: str):
		before = len(self.movies)
		self.movies = [movie for movie in self.movies if movie.title.lower() != title.lower()]
		after = len(self.movies)
		if before == after:
			print(f"No movie titled '{title}' was found to delete.")
		else:
			print(f"Deleted movie '{title}'.")

	def list_movies(self):
		if not self.movies:
			print("No movies in your collection.")
			return
		for m in self.movies:
			print(m)

	def stats(self):
		ratings = [float(m.rating) for m in self.movies if m.rating != 'N/A' and m.rating != 'N/A']
		if not ratings:
			print("No valid ratings available to calculate stats.")
			return
		avg = sum(ratings) / len(ratings)
		print(f"Average IMDB Rating: {avg:.2f}")


# Command-line interface
if __name__ == '__main__':
	import sys

	collection = MovieCollection()


	def print_help():
		print("Commands:")
		print("  add <movie title>    - Add a movie by title (fetches from OMDb)")
		print("  delete <movie title> - Delete a movie by title")
		print("  list                 - List all movies")
		print("  stats                - Show average rating stats")
		print("  quit                 - Exit the application")


	print("Welcome to Movie Manager!")
	print_help()

	while True:
		try:
			cmd = input("\n> ").strip().split(' ', 1)
			action = cmd[0].lower()
			arg = cmd[1] if len(cmd) > 1 else ''

			if action == 'add' and arg:
				try:
					collection.add_movie(arg)
				except ValueError as ve:
					print(ve)
				except requests.exceptions.RequestException as re:
					print(re)
			elif action == 'delete' and arg:
				collection.delete_movie(arg)
			elif action == 'list':
				collection.list_movies()
			elif action == 'stats':
				collection.stats()
			elif action == 'help':
				print_help()
			elif action in ('quit', 'exit'):
				print("Goodbye!")
				sys.exit(0)
			else:
				print("Unknown command. Type 'help' for a list of commands.")
		except KeyboardInterrupt:
			print("\nGoodbye!")
			sys.exit(0)
