import requests
from typing import Dict, Generator
from bs4 import BeautifulSoup
from cache import cache_using

IMDB_HOST = "https://www.imdb.com"
GENRES_PAGE = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"


@cache_using("redis")
def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def get_soup_for_page(url: str) -> BeautifulSoup:
    return BeautifulSoup(get_html(url), 'html.parser')


def get_imdb_movies(max_movies: int, movies_per_genre: int) -> Generator:
    """
    Crawl and parse IMDB to populate movies database
    :param max_movies: maximum movies to crawl
    :param movies_per_genre: how many movies to fetch for each genre
    :return: generator for movie data
    """
    movie_urls = crawl_imdb_movies(max_movies=max_movies, movies_per_genre=movies_per_genre)
    for url, genre in movie_urls:
        yield parse_movie_page(url, genre)


def parse_movie_page(movie_url: str, genre: str) -> Dict[str, str]:
    """
    Extract movie information from a imdb movie page
    :param movie_url: the imdb url for a particular movie
    :param genre: the genre name
    :return: structured data from movie
    """
    movie_page = get_soup_for_page(movie_url)

    # title and id
    movie_id = movie_url.split("/")[-2]
    title = movie_page.find("div", class_="title_wrapper").find("h1").get_text(";", strip=True).split(";")[0]

    # director and stars
    credit_summary_elements = movie_page.find_all("div", class_="credit_summary_item")
    director = credit_summary_elements[0].find("a").text if len(credit_summary_elements) > 0 else ""
    if len(credit_summary_elements) > 2:
        stars_links = credit_summary_elements[2].find_all("a")
        stars = [str(elem.text) for elem in stars_links[:-1]]
    else:
        stars = []
    movie_data = {
        "id": movie_id,
        "title": title,
        "director": director,
        "stars": stars,
        "genre": genre.strip()
    }
    print(movie_data)
    return movie_data


def crawl_imdb_movies(max_movies=1000, movies_per_genre=100) -> Generator:
    """
    Start crawling from GENRES_PAGE to enter each genre and yield movie_url with its genre
    :param max_movies: maximum movies to crawl
    :param movies_per_genre: how many movies to fetch for each genre
    :return: generator of tuple (movie_url, genre_name)
    """
    movie_counter = 0
    genres_page = get_soup_for_page(GENRES_PAGE)
    movies_genres_section = genres_page.find_all("div", class_="article")[5]
    for a_link in movies_genres_section.find_all("a"):
        if movie_counter == max_movies:
            break
        genre_url = IMDB_HOST + a_link["href"]
        genre_name = a_link.text
        for movie_url in crawl_genre_page(genre_url, movies_per_genre, 0):
            movie_counter += 1
            yield movie_url, genre_name


def crawl_genre_page(genre_url: str, movies_per_genre: int, counter: int) -> Generator:
    """
    Recursive function
    :param counter:
    :param movies_per_genre:
    :param genre_url:
    :return:
    """
    print(f"CRAWLING GENRE {genre_url}")
    genre_page = get_soup_for_page(genre_url)
    next_page = genre_page.find("a", class_="lister-page-next next-page")
    for movies_element in genre_page.find_all("div", class_="lister-item mode-advanced"):
        if counter >= movies_per_genre:
            break
        a_link = movies_element.find("h3", class_="lister-item-header").find("a")
        counter += 1
        yield IMDB_HOST + a_link["href"]
    if next_page and counter < movies_per_genre:
        next_page_url = IMDB_HOST + next_page["href"]
        return crawl_genre_page(next_page_url, movies_per_genre, counter)
