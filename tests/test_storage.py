# test_storage.py
from storage_json import StorageJson

def main():
    storage = StorageJson('../test_movies.json')
    assert storage.list_movies() == {}
    storage.add_movie('Matrix', 1999, 8.7, '/img/matrix.jpg')
    movies = storage.list_movies()
    assert 'Matrix' in movies and movies['Matrix']['rating'] == 8.7
    storage.update_movie('Matrix', 9.0)
    assert storage.list_movies()['Matrix']['rating'] == 9.0
    storage.delete_movie('Matrix')
    assert storage.list_movies() == {}
    print("All tests passed!")

if __name__ == '__main__':
    main()
