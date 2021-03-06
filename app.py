from flask import Flask, request

from imdb.database import search_imdb_database

app = Flask(__name__)


@app.route('/')
def index():
    from imdb.database import database_size
    if database_size() == 0:
        populate_database()

    search = request.args.get('search', '')
    movies = search_imdb_database(search)
    return {
        "success": True,
        "databaseSize": database_size(),
        "message": f"You searched for {search}",
        "results": [movie["title"] for movie in movies.values()]
    }


@app.route("/populate")
def populate():
    from imdb.database import database_size
    max_movies = int(request.args.get('max', '1000'))
    populate_database(max_movies)
    return {
        "success": True,
        "message": "database populated",
        "databaseSize": database_size()
    }


def populate_database(max_movies=1000):
    from imdb.crawler import get_imdb_movies
    get_imdb_movies(max_movies)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
