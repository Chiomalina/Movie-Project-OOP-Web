from storage_json import StorageJson
from movie_app import MovieApp

def main():
    # 1) Test with john.json
    john_storage = StorageJson('john.json')
    john_app = MovieApp(john_storage)
    print("=== Running app for John ===")
    john_app.run()  # should immediately break (as per our stub), but must not error

    # 2) Test with sara.json
    sara_storage = StorageJson('sara.json')
    sara_app = MovieApp(sara_storage)
    print("=== Running app for Sara ===")
    sara_app.run()  # likewise should start & stop cleanly

if __name__ == "__main__":
    main()
