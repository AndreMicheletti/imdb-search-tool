from imdb.crawler import crawl_imdb_movies


def get_imdb_movies(max_movies, movies_per_genre):
    """
    Crawl and parse IMDB to populate movies database
    :param movies_per_genre: how many movies to fetch for each genre
    :return: generator for movie data
    """
    movie_urls = crawl_imdb_movies(max_movies=max_movies, movies_per_genre=movies_per_genre)
    for url, genre in movie_urls:
        yield parse_movie_page(url, genre)


def parse_movie_page(movie_url, genre):
    """
    Extract movie information from a imdb movie page
    :param movie_page: BeautifulSoup object
    :return: structured data from movie
    """
    from imdb.crawler import get_soup_for_page
    movie_page = get_soup_for_page(movie_url)

    # title and id
    id = movie_url.split("/")[-2]
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
        "id": id,
        "title": title,
        "director": director,
        "stars": stars,
        "genre": genre.strip()
    }
    print(movie_data)
    return movie_data
