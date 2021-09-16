import json
import math

from more_itertools import chunked
from pathlib import Path
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib.parse import urljoin

JSON_FILE = 'books_info.json'
TEMPLATE_HTML = 'template.html'
PAGES_FOLDER = 'pages'
DEFAULT_PAGE_NAME = 'index'
BOOKS_QUANTITY_ON_PAGE = 10
BASE_URL = '/'


def get_pages_info(books: list) -> list:
    pages = []
    for page in range(1, math.ceil(len(books) / BOOKS_QUANTITY_ON_PAGE)):
        pages.append({"number": page,
                      "link": urljoin(BASE_URL, f'{PAGES_FOLDER}/{DEFAULT_PAGE_NAME}{page}.html')
                      })
    return pages


def update_urls_in_books(books: list, base_url: str = BASE_URL):
    for book in books:
        book['img_src'] = urljoin(base_url, book.get('img_src'))
        book['book_path'] = urljoin(base_url, book.get('book_path'))
    return books


def save_page(rendered_page: str,
              page_index: int,
              folder: str = PAGES_FOLDER,
              name: str = DEFAULT_PAGE_NAME):
    Path.mkdir(Path(folder), exist_ok=True, parents=True)
    with open(Path(folder) / f'{name}{page_index}.html', 'w') as file:
        file.write(rendered_page)


def split_books_by_pages(books: list,
                         folder: str = PAGES_FOLDER,
                         file_name: str = DEFAULT_PAGE_NAME,
                         books_quantity_on_page: int = BOOKS_QUANTITY_ON_PAGE) -> None:
    """Read books and save split html-pages by paths ./folder/index{page_index}.html."""
    for page_index, books_chunk in enumerate(chunked(books, books_quantity_on_page), 1):
        template = env.get_template(TEMPLATE_HTML)
        rendered_page = template.render(books=update_urls_in_books(books_chunk),
                                        pages=get_pages_info(books))
        save_page(rendered_page, page_index, folder, file_name)


def on_reload():
    template = env.get_template(TEMPLATE_HTML)
    rendered_page = template.render(
        books=update_urls_in_books(books),
        pages=get_pages_info(books)
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    split_books_by_pages(books)


if __name__ == '__main__':
    with open(JSON_FILE) as file_data:
        books = json.loads(file_data.read())

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
