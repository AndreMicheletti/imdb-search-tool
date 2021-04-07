from flask import Flask
from flask import request

from imdb.database import search_imdb_database
app = Flask(__name__)


@app.route('/')
def hello_world():
    search = request.args.get('search', '')
    return {
        "success": True,
        "message": f"You searched for {search}",
        "results": search_imdb_database(search)
    }


if __name__ == '__main__':
    app.run(debug=True)
