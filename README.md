# IMDB Search Tool

## How to run

Requirements:
 - docker
 
Instructions:
 - Clone the repository
 - Build the docker image with `docker build . -t imdb_andre`
 - Run the docker image with `docker run -p 5000:5000 imdb_andre`
 - Use the API with `curl -X GET 'http://0.0.0.0:5000/?search=spielberg hanks'`
