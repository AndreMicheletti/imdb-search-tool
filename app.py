from flask import Flask
from flask import request

from imdb.database import search_imdb_database
app = Flask(__name__)


def populate_database():
    from imdb.parser import get_imdb_movies
    from imdb.database import index_movie_to_database, imbd_database
    if len(imbd_database) <= 0:
        print("VAI TER Q CRAWLAR")
        for movie in get_imdb_movies(1000, movies_per_genre=100):
            index_movie_to_database(movie)


@app.route('/')
def index():
    from imdb.database import imbd_database
    populate_database()
    search = request.args.get('search', '')
    movies = search_imdb_database(search)
    return {
        "success": True,
        "databaseSize": len(imbd_database.keys()),
        "message": f"You searched for {search}",
        "results": [movie["title"] for movie in movies.values()]
    }


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
