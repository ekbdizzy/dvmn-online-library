import requests
from bs4 import BeautifulSoup
from urllib import parse
import argparse
import logging


def parse_book_page(html: bytes) -> dict:
    """Parse title, author, image_link and genres from html."""
    soup = BeautifulSoup(html, 'lxml')
    title, author = [i.strip() for i in (soup.find('h1').text.split("::"))]
    image_link = soup.find("div", class_="bookimage").find("img")['src']
    genres = [genre.text for genre in soup.find("span", class_="d_book").find_all("a")]
    return {
        "title": title,
        "author": author,
        "image_link": parse.urljoin("https://tululu.org", image_link),
        "genres": genres,
    }


def parse_books(start_id: int, end_id: int):
    for book_id in range(start_id, end_id + 1):
        url = f"https://tululu.org/b{book_id}/"
        try:
            response = requests.get(f"{url}")
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            logging.exception(f"Connection error: failed to establish connection to {url}")
            continue

        except requests.exceptions.HTTPError as e:
            logging.exception(e)
            continue

        if not response.history:
            book_info = parse_book_page(response.content)
            print(f'Название: {book_info.get("title")}\nАвтор: {book_info.get("author")}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Parse books_info from tululu.org.")
    parser.add_argument("--start_id", metavar="start_id", type=int, default=0, help="first book_id of parse list.")
    parser.add_argument("--end_id", metavar="--end_id", type=int, default=10, help="last book_id of parse list.")
    args = parser.parse_args()
    parse_books(args.start_id, args.end_id)

    logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', level=logging.INFO)
