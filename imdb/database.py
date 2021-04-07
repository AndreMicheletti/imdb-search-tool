
imbd_database = []


def search_imdb_database(search_query):
    from imdb.crawler import get_imdb_movies
    if len(imbd_database) <= 0:
        get_imdb_movies(imbd_database)

    print("database: ", imbd_database)
    return []
