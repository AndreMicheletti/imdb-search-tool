import requests
from bs4 import BeautifulSoup
from cache import redis_cache_by_first_arg

IMDB_HOST = "https://www.imdb.com"
GENRES_PAGE = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"


@redis_cache_by_first_arg
def get_html(url):
    response = requests.get(url)
    return response.text


def get_soup_for_page(url):
    return BeautifulSoup(get_html(url), 'html.parser')


def crawl_imdb_movies(max_movies=1000, movies_per_genre=100):
    movie_counter = 0
    genres_page = get_soup_for_page(GENRES_PAGE)
    movies_genres_section = genres_page.find_all("div", class_="article")[5]
    for a_link in movies_genres_section.find_all("a"):
        if movie_counter == max_movies:
            break
        genre_counter = 0
        genre_url = IMDB_HOST + a_link["href"]
        genre_name = a_link.text
        print(f"CRAWLING TOP LEVEL: GENRE {genre_url}")
        for movie_url in crawl_genre_page(genre_url):
            if genre_counter == movies_per_genre or movie_counter == max_movies:
                break
            genre_counter += 1
            movie_counter += 1
            yield (movie_url, genre_name)


def crawl_genre_page(genre_url):
    print(f"CRAWLING GENRE {genre_url}")
    genre_page = get_soup_for_page(genre_url)
    next_page = genre_page.find("a", class_="lister-page-next next-page")
    next_page_url = IMDB_HOST + next_page["href"]
    for movies_element in genre_page.find_all("div", class_="lister-item mode-advanced"):
        a_link = movies_element.find("h3", class_="lister-item-header").find("a")
        yield IMDB_HOST + a_link["href"]
    return crawl_genre_page(next_page_url)
