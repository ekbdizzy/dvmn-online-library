import pathlib
import requests

BOOKS_DIR = pathlib.Path('./books')
BOOKS_SITE_URL = "https://tululu.org/txt.php"
BOOKS_QUANTITY = 10


def fetch_books(books_quantity):
    for book_id in range(1, books_quantity + 1):
        response = requests.get(BOOKS_SITE_URL, params={"id": book_id})
        response.raise_for_status()
        if not response.history:
            yield book_id, response.text


def main():
    pathlib.Path.mkdir(BOOKS_DIR, exist_ok=True)
    for book_id, book_text in fetch_books(BOOKS_QUANTITY):
        with open(pathlib.Path(BOOKS_DIR / f"{book_id}.txt"), "w") as book_file_data:
            book_file_data.write(book_text)


if __name__ == '__main__':
    main()
