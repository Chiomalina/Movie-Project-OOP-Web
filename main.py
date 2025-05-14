# main.py
"""
Entry point for the Movie Project application.
"""

from storage_csv import StorageCsv
from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """Create storage, initialize MovieApp, and start the application."""
    # You can swap out StorageJson for another IStorage implementation in the future
    #storage = StorageJson('movies.json')
    storage = StorageCsv('movies.csv')
    app = MovieApp(storage)
    app.run()


if __name__ == '__main__':
    main()
