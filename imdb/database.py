
imbd_database = {}
imdb_id_index = []


def index_movie_to_database(movie_data):
    if movie_data["id"] not in imdb_id_index:
        keywords = extract_keywords(movie_data)
        imbd_database[keywords] = movie_data
        imdb_id_index.append(movie_data["id"])


def extract_keywords(movie_data):
    keywords = movie_data["title"].split(" ")
    keywords.append(movie_data["genre"].lower())
    keywords.extend(movie_data["director"].split(" "))
    for star in movie_data["stars"]:
        keywords.extend(star.split(" "))
    return " ".join(map(lambda x: x.lower(), keywords))


def search_imdb_database(search_query):
    keywords = list(map(lambda x: x.lower(), search_query.split(" ")))
    clone_database = {**imbd_database}
    return filter_database_with_keywords(clone_database, keywords)


def filter_database_with_keywords(database: dict, keywords: list):
    if len(keywords) == 0:
        return database
    keyword = keywords.pop()
    return filter_database_with_keywords(
        {k: v for k, v in database.items() if keyword in k},
        keywords
    )
