import requests
from bs4 import BeautifulSoup

IMDB_HOST = "https://www.imdb.com"
GENRES_PAGE = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"


def get_soup_for_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_imdb_movies(database):
    genres_urls = []
    genres_page = get_soup_for_page(GENRES_PAGE)
    movies_genres_section = genres_page.find_all("div", class_="article")[5]
    for a_link in movies_genres_section.find_all("a"):
        genres_urls.append(IMDB_HOST + a_link["href"])
    print(f"CRAWLING TOP LEVEL: {len(genres_urls)} GENRES")
    for genre_url in genres_urls:
        crawl_genre_page(database, genre_url)
    return True


def crawl_genre_page(database, genre_url):
    print(f"CRAWLING GENRE {genre_url}")
    movies_urls = []
    genre_page = get_soup_for_page(genre_url)
    for movies_element in genre_page.find_all("div", class_="lister-item mode-advanced"):
        a_link = movies_element.find("h3", class_="lister-item-header").find("a")
        movies_urls.append(IMDB_HOST + a_link["href"])
    for movie_url in movies_urls:
        crawl_movie_page(database, movie_url)


def crawl_movie_page(database, movie_url):
    print(f"CRAWLING MOVIE {movie_url}")
    movie_page = get_soup_for_page(movie_url)

    title = movie_page.find("div", class_="title_wrapper").find("h1").get_text(";", strip=True).split(";")[0]
    credit_summary_elements = movie_page.find_all("div", class_="credit_summary_item")
    director = credit_summary_elements[0].find("a").text
    stars_links = credit_summary_elements[2].find_all("a")
    stars = [str(elem.text) for elem in stars_links[:-1]]
    movie_data = {
        "title": title,
        "director": director,
        "stars": stars
    }
    print(movie_data)
    database.append(movie_data)
