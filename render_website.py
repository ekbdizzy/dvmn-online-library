import json
import math

from more_itertools import chunked
from pathlib import Path
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape

JSON_FILE = 'books_info.json'
TEMPLATE = './assets/templates/template.html'
PAGES_FOLDER = 'pages'
DEFAULT_PAGE_NAME = 'index'
BOOKS_QUANTITY_ON_PAGE = 10


def get_pages(books: list) -> list:
    pages = []
    for page in range(1, math.ceil(len(books) / BOOKS_QUANTITY_ON_PAGE) + 1):
        pages.append({"number": page,
                      "link": f'{DEFAULT_PAGE_NAME}{page}.html'
                      })
    return pages


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
        template = env.get_template(TEMPLATE)
        rendered_page = template.render(books=books_chunk,
                                        pages=get_pages(books),
                                        current_page=page_index)
        save_page(rendered_page, page_index, folder, file_name)


def on_reload():
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
    server.watch('assets/', on_reload)
    server.serve(root='.')
