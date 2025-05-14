# movie_app.py

import random
import matplotlib.pyplot as plt
from colorama import Fore, init
from rapidfuzz import process, fuzz

from istorage import IStorage
from storage_json import StorageJson  # For type reference if needed
from movies import (
    prompt_title,
    prompt_rating,
    prompt_year,
    prompt_choice,
    title as print_title,
    display_menu
)

class MovieApp:
    """Main application class for the Movie App, handling user commands via a storage backend."""

    def __init__(self, storage: IStorage):
        """Initialize the MovieApp with a storage implementation."""
        init(autoreset=True)
        self._storage = storage

    def _command_list_movies(self):
        """List all movies with their year and rating."""
        movies = self._storage.list_movies()
        print(Fore.CYAN + f"\n{len(movies)} movies in total")
        for title_str, info in movies.items():
            print(Fore.GREEN + f"{title_str} ({info['year']}): {info['rating']}")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_add_movie(self):
        """Add a new movie; prompts for title, year, rating, and poster."""
        title_str = prompt_title("Enter new movie name: ")
        year_val = prompt_year()
        rating_val = prompt_rating()
        poster_path = prompt_title("Enter poster file path: ")
        try:
            self._storage.add_movie(title_str, year_val, rating_val, poster_path)
            print(Fore.GREEN + f"{title_str} ({year_val}) added with rating {rating_val}!")
        except Exception as e:
            print(Fore.RED + str(e))
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_delete_movie(self):
        """Delete a movie; prompts for title."""
        title_str = prompt_title("Enter movie name to delete: ")
        try:
            self._storage.delete_movie(title_str)
            print(Fore.GREEN + f"{title_str} successfully deleted.")
        except KeyError:
            print(Fore.RED + f"Movie '{title_str}' not found.")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_update_movie(self):
        """Update a movie's rating; prompts for title and new rating."""
        title_str = prompt_title("Enter movie name to update: ")
        rating_val = prompt_rating()
        try:
            self._storage.update_movie(title_str, rating_val)
            print(Fore.GREEN + f"{title_str} rating updated to {rating_val}.")
        except KeyError:
            print(Fore.RED + f"Movie '{title_str}' not found.")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_movie_stats(self):
        """Display average, median, best and worst movie statistics."""
        movies = self._storage.list_movies()
        ratings = [info['rating'] for info in movies.values()]
        if not ratings:
            print(Fore.RED + "No movies in the database.")
        else:
            avg = sum(ratings) / len(ratings)
            median = sorted(ratings)[len(ratings)//2]
            best = max(movies, key=lambda t: movies[t]['rating'])
            worst = min(movies, key=lambda t: movies[t]['rating'])
            print(Fore.CYAN + f"\nAverage Rating: {avg:.1f}")
            print(Fore.CYAN + f"Median Rating : {median:.1f}")
            print(Fore.GREEN + f"Best Movie    : {best} ({movies[best]['year']}) — {movies[best]['rating']}")
            print(Fore.RED + f"Worst Movie   : {worst} ({movies[worst]['year']}) — {movies[worst]['rating']}")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_random_movie(self):
        """Pick and display a random movie."""
        movies = self._storage.list_movies()
        if movies:
            movie_title = random.choice(list(movies))
            info = movies[movie_title]
            print(Fore.GREEN + f"Your movie for tonight: {movie_title} ({info['year']}) — {info['rating']}")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_search_movie(self):
        """Search for movies by fuzzy matching; prompts for search term."""
        term = prompt_title("Enter part of movie name to search: ")
        movies = self._storage.list_movies()
        if term in movies:
            info = movies[term]
            print(Fore.GREEN + f"Found: {term} ({info['year']}) — {info['rating']}")
        else:
            matches = process.extract(term, movies.keys(), scorer=fuzz.ratio, limit=5)
            suggestions = [m for m, score, _ in matches if score >= 50]
            if suggestions:
                print(Fore.YELLOW + "\nNo exact match. Did you mean:")
                for m in suggestions:
                    info = movies[m]
                    print(Fore.CYAN + f" {m} ({info['year']}) — {info['rating']}")
            else:
                print(Fore.RED + "No similar movies found.")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_sort_by_rating(self):
        """Show movies sorted by descending rating."""
        movies = self._storage.list_movies()
        sorted_list = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        print(Fore.CYAN + "\nMovies sorted by rating:")
        for t, info in sorted_list:
            print(Fore.GREEN + f"{t} ({info['year']}) — {info['rating']}")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_sort_by_year(self):
        """Show movies sorted by release year, asking latest-first or oldest-first."""
        movies = self._storage.list_movies()
        while True:
            ans = input(Fore.MAGENTA + "Show latest movies first? (y/n): ").strip().lower()
            if ans in ('y', 'n'):
                break
            print(Fore.RED + "⚠️ Please enter 'y' or 'n'.")
        reverse = ans == 'y'
        sorted_list = sorted(movies.items(), key=lambda x: x[1]['year'], reverse=reverse)
        order_desc = "latest first" if reverse else "oldest first"
        print(Fore.CYAN + f"\nMovies sorted by year ({order_desc}):")
        for t, info in sorted_list:
            print(Fore.GREEN + f"{t} ({info['year']}) — {info['rating']}")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_filter_movies(self):
        """Filter movies by minimum rating, start year and end year."""
        movies = self._storage.list_movies()
        # Prompt for criteria
        while True:
            input_rating = input(Fore.MAGENTA + "Enter minimum rating (leave blank for no minimum): ").strip()
            if not input_rating:
                min_rating = None
                break
            try:
                val = float(input_rating)
                if 0.0 <= val <= 10.0:
                    min_rating = val
                    break
                print(Fore.RED + "⚠️ Rating must be between 0.0 and 10.0.")
            except ValueError:
                print(Fore.RED + "⚠️ Invalid rating format.")
        while True:
            input_start = input(Fore.MAGENTA + "Enter start year (leave blank for no start year): ").strip()
            if not input_start:
                start_year = None
                break
            if input_start.isdigit() and len(input_start) == 4:
                start_year = int(input_start)
                break
            print(Fore.RED + "⚠️ Year must be a four-digit number.")
        while True:
            input_end = input(Fore.MAGENTA + "Enter end year (leave blank for no end year): ").strip()
            if not input_end:
                end_year = None
                break
            if input_end.isdigit() and len(input_end) == 4:
                end_year = int(input_end)
                break
            print(Fore.RED + "⚠️ Year must be a four-digit number.")
        # Filter
        filtered = []
        for title_str, info in movies.items():
            rating_val, year_val = info['rating'], info['year']
            if min_rating is not None and rating_val < min_rating:
                continue
            if start_year is not None and year_val < start_year:
                continue
            if end_year is not None and year_val > end_year:
                continue
            filtered.append((title_str, year_val, rating_val))
        # Display
        print(Fore.CYAN + "\nFiltered Movies:")
        if filtered:
            for t, y, r in filtered:
                print(Fore.GREEN + f"{t} ({y}): {r}")
        else:
            print(Fore.YELLOW + "No movies match the criteria.")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _command_create_rating_histogram(self):
        """Generate and save a histogram of movie ratings; prompts for filename."""
        movies = self._storage.list_movies()
        ratings = [info['rating'] for info in movies.values()]
        filename = prompt_title("Enter filename for histogram (e.g., ratings.png): ")
        plt.figure(figsize=(10, 8))
        plt.hist(ratings, bins=20, edgecolor='black', alpha=0.7)
        plt.title("Movie Ratings Histogram")
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.savefig(filename)
        print(Fore.GREEN + f"Histogram saved to {filename}")
        input(Fore.MAGENTA + "\nPress enter to continue")

    def _generate_website(self):
        """Generate a static website representation of the movie database."""
        # TODO: implement HTML generation
        pass

    def run(self):
        """Run the main loop: display menu, prompt choice, execute commands."""
        while True:
            print_title()
            display_menu()
            choice = prompt_choice()
            if choice == 0:
                print(Fore.CYAN + "Bye!")
                break
            elif choice == 1:
                self._command_list_movies()
            elif choice == 2:
                self._command_add_movie()
            elif choice == 3:
                self._command_delete_movie()
            elif choice == 4:
                self._command_update_movie()
            elif choice == 5:
                self._command_movie_stats()
            elif choice == 6:
                self._command_random_movie()
            elif choice == 7:
                self._command_search_movie()
            elif choice == 8:
                self._command_sort_by_rating()
            elif choice == 9:
                self._command_create_rating_histogram()
            elif choice == 10:
                self._command_sort_by_year()
            elif choice == 11:
                self._command_filter_movies()
            # Future: elif choice maps to generate website etc.
