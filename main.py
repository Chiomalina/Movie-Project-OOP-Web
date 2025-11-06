""" entrypoint that wires StorageJson -> MovieApp"""

from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main() -> None:
    """
    Try per-user storage files to validate “multiple files” architecture:
    storage = StorageJson("john.json")
    storage = StorageJson("sara.json")
    """

    storage_csv = StorageCsv("movies.csv")
    storage_json = StorageJson("movies.json")

    app = MovieApp(storage_csv)
    app.run()


if __name__ == "__main__":
    main()
