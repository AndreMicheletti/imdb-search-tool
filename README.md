# IMDB Search Tool

Made with `python`, `flask`

## Comments

#### What has been done

The crawling/parsing step is very straight forward, the algorithm takes
how many movies it should fetch and starts crawling the IMDB website,
starting at a predefined listing page, and stopping when it reaches the
given limit or there are no more pages.

The data indexing part was more interesting, and as the problem
states, I should assume a not so large data scale, and it was advised
to implement a solution rather than going for external tools.

So the program has a global `dict` (which means all data stay in 
execution memory) that serves as the database. Then each movie receives
a `index_key` made up by all its _keywords_ in a single `string`, and is
added to the global dict using this `index_key`

To search the database, the program receives the search query and split it
into keywords _(space-delimited)_. Then it selects the movies which the `index_key`
contains all keywords.

**Cache**

I've implemented a very simple cache using decorators with two "store"
options: `in-memory` and `redis`. The cache is used to store the IMDB pages
HTML to speed up and avoid going external too many times.

The `Dockerfile` defaults to in-memory. If you want to use redis, change
the line `ENV CACHE_TYPE=memory` to `ENV CACHE_TYPE=redis` in the `Dockerfile`
and bind the redis port to the `docker run` command.  

#### Thoughts on improvements

**Data indexing/lookup**

Could use a more optimized indexing strategy, such as using binary 
search trees to avoid stepping into every document in the database everytime.
And for every document, we need to traverse through the entire string trying
to find the keyword, which also increases the time complexity for searching.

Also, given the problem domain, one could use databases such as 
**ElasticSearch** that focus on indexing and searching documents to
be queryable using keywords, text-matching and "similarity".

**Crawling**

For better crawling performance, one could implement parallel execution and
use multiples threads to crawl, parse and index the IMDB website.

Using async frameworks such as `tornado` or `sanic`, or using background workers
with `celery` could achieve this.

**Unit Testing**

Tests are always welcome. 

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

`curl -X GET 'http://0.0.0.0:5000/populate?max=1000'`
