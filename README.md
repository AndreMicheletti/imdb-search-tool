# IMDB Search Tool

## How to run

Requirements:
 - docker
 
Instructions:
 - Clone the repository
 - Build the docker image with `docker build . -t imdb_andre`
 - Run the docker image with `docker run -p 5000:5000 imdb_andre`
 - Use the API with `curl -X GET 'http://0.0.0.0:5000/?search=spielberg hanks'`
 
The first request will populate the database, so it may take a while.

You can request the API to populate with a custom number of movies using:

`curl -X GET 'http://0.0.0.0:5000/populate?max=1000&per_genre=100'`

Params: 
- `max` is the maximum number of movies to crawl into.
- `per_genre` is the maximum number of movies to crawl at each genre.
