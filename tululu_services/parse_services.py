import requests
from urllib import parse
from typing import Optional
from pathlib import Path
from bs4 import BeautifulSoup
import logging


def is_redirect(response):
    return response.history


def parse_book_title(url: str) -> Optional[str]:
    response = requests.get(url)
    response.raise_for_status()

    if is_redirect(response):
        return

    soup = BeautifulSoup(response.text, "lxml")
    title, _ = soup.find('h1').text.split("::")
    return title.strip()


def parse_genres(url):
    response = requests.get(url)
    response.raise_for_status()

    if is_redirect(response):
        return

    soup = BeautifulSoup(response.content, "lxml")
    genres = [genre.text for genre in soup.find("span", class_="d_book").find_all("a")]
    print(genres)


def parse_file_name_from_url(url: str) -> str:
    return parse.unquote(Path(parse.urlsplit(url).path).name)


def parse_cover_image_link(soup: BeautifulSoup):
    image_link = soup.find("div", class_="bookimage").find("img")['src']
    return parse.urljoin("https://tululu.org", image_link)


def parse_book_page(html: bytes) -> dict:
    """Parse title, author, image_link and genres from html."""
    soup = BeautifulSoup(html, 'lxml')
    title, author = [book_info.strip() for book_info in (soup.find('h1').text.split("::"))]
    image_link = parse_cover_image_link(soup)
    genres = [genre.text for genre in soup.find("span", class_="d_book").find_all("a")]
    return {
        "title": title,
        "author": author,
        "image_link": image_link,
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

        if not is_redirect(response):
            book_info = parse_book_page(response.content)
            print(f'Название: {book_info.get("title")}\nАвтор: {book_info.get("author")}\n')
