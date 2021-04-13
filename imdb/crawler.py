import requests
import os
from typing import Dict, Generator
from bs4 import BeautifulSoup
from cache import cache_using

IMDB_HOST = "https://www.imdb.com"
TOP_PAGE = "https://www.imdb.com/search/title/?title_type=feature&view=simple"


@cache_using(os.getenv("CACHE_TYPE", "memory"))
def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def get_soup_for_page(url: str) -> BeautifulSoup:
    """ Get and parse HTML from url to return a BeautifulSoup object """
    return BeautifulSoup(get_html(url), 'html.parser')


def get_imdb_movies(max_movies: int):
    """
    Crawl, parse and index IMDB to populate movies database
    :param max_movies: maximum movies to crawl
    :return: generator for movie data
    """
    from imdb.database import index_movie_to_database
    movie_count = 0
    for url in crawl_imdb_listing_page(TOP_PAGE):
        if movie_count == max_movies:
            break
        movie_data = parse_movie_page(url)
        if index_movie_to_database(movie_data):
            movie_count += 1


def crawl_imdb_listing_page(url: str) -> Generator:
    """
    Generator function to keep crawling the listing pages, yielding the found movies urls.
    :param url: starting url to crawl from (must be a listing page with next button)
    :return: generator that yields movie urls
    """
    next_url = url
    while next_url:
        print(f"CRAWLING URL {next_url}")
        listing_page = get_soup_for_page(next_url)
        for movies_element in listing_page.find_all("div", class_="lister-item mode-simple"):
            a_link = movies_element.find("span", class_="lister-item-header").find("a")
            yield IMDB_HOST + a_link["href"]
        next_url = listing_page.find("a", class_="lister-page-next next-page")
        next_url = IMDB_HOST + next_url["href"] if next_url else None


def parse_movie_page(movie_url: str) -> Dict[str, str]:
    """
    Extract movie information from a imdb movie page
    :param movie_url: the imdb url for a particular movie
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
    }
    print(movie_data)
    return movie_data
