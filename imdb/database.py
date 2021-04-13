import json
from typing import Dict

imbd_database = {}
imdb_id_index = []


def database_size() -> int:
    """ Return quantity of records in database """
    return len(imbd_database.keys())


def index_movie_to_database(movie_data: Dict[str, str]):
    """
    Indexes a new movie record to the database, ignoring movies that were already indexed.
    :param movie_data: dict of movie data structure
    """
    if movie_data["id"] in imdb_id_index:
        return False
    index_key = generate_movie_index_key(movie_data)
    imbd_database[index_key] = movie_data
    imdb_id_index.append(movie_data["id"])
    return True


def generate_movie_index_key(movie_data: Dict[str, str]) -> str:
    """
      Generates a index key for the movie data. The key is based on all searchable
    keywords in lowercase and separated by white space
    :param movie_data: dict of movie data structure
    :return: the index key for that movie
    """
    keywords = movie_data["title"].split(" ")
    keywords.extend(movie_data["director"].split(" "))
    for star in movie_data["stars"]:
        keywords.extend(star.split(" "))
    return " ".join(map(lambda x: x.lower(), keywords))


def search_imdb_database(search_query):
    keywords = list(map(lambda x: x.lower(), search_query.split(" ")))
    return {
        index_key: movie for index_key, movie in imbd_database.items()
        if all([(keyword in index_key) for keyword in keywords])
    }


def filter_database_with_keywords(database: dict, keywords: list) -> dict:
    """
      Function that filters the database using keywords provided.
    Each database record is selected if it contains the keyword in its
    index key.
    :param database: a dict representing the database
    :param keywords: a list of lowercase keywords
    :return: the filtered database
    """
    return {
        index_key: movie for index_key, movie in database.items()
        if all([(keyword in index_key) for keyword in keywords])
    }


def save_database():
    """ Util function to save database to a file """
    with open("./database.json", "w") as f:
        json.dump(imbd_database, f)
    print("DATABASE SAVED")
