import sys
from typing import Optional, List
from urllib import parse
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_last_page_for_category(url: str) -> int:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    try:
        end_page = soup.select("a.npage")[-1]
        return int(end_page.text)
    except IndexError:
        return 1


def has_link_to_download_txt(soup, book_id) -> bool:
    """Проверяет, есть ли ссылка на скачивание txt-файла."""
    link = [a for a in soup.select('a') if a['href'] == f"/txt.php?id={book_id}"]
    return bool(link)


def parse_file_name_from_url(url: str) -> str:
    return parse.unquote(Path(parse.urlsplit(url).path).name)


def parse_cover_image_link(soup: BeautifulSoup) -> str:
    image_link = soup.select_one("div.bookimage img")['src']
    return parse.urljoin("https://tululu.org", str(image_link))


def parse_books_ids(soup: BeautifulSoup) -> List[int]:
    """Парсит id всех книг из HTML-страницы со списком книг."""
    ids = []
    for book in soup.select("table.d_book"):
        book_relative_link = book.select_one("a")["href"]
        book_id = "".join(filter(lambda x: x.isdigit(), book_relative_link))
        ids.append(int(book_id))
    return ids


def parse_book_page(soup: BeautifulSoup) -> dict:
    """Парсит title, author, image_link and genres из HTML-страницы с книгой."""

    title, author = [title_and_author.strip() for title_and_author in (soup.select_one('h1').text.split("::"))]
    image_link = parse_cover_image_link(soup)
    genres = [genre.text for genre in soup.select("span.d_book a")]
    comments = [comment.text for comment in soup.select("div.texts span.black")]
    return {
        "title": title,
        "author": author,
        "image_link": image_link,
        "genres": genres,
        "comments": comments
    }


def update_book_info(book_info: dict, filepath: str, images_folder='images', skip_images=False) -> Optional[dict]:
    """Проверяет на наличие скачанной книги, заменяет в book_data пути к файлам книги и обложки
    и убирает ссылку на обложку."""
    if not filepath:
        return
    if not skip_images:
        book_info['img_src'] = str(Path(Path(images_folder) / book_info.get('image_link').split('/')[-1]))
    del book_info['image_link']
    book_info['book_path'] = str(filepath)
    return book_info
