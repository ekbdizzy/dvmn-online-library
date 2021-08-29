from pathlib import Path
from typing import Optional
import requests
from pathvalidate import sanitize_filename
import logging
from parse_services import (parse_file_name_from_url,
                            is_redirect,
                            parse_book_page,
                            update_book_info)


def download_txt(book_id, filename, folder='books', url="https://tululu.org/txt.php"):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на страницу, с которой нужно скачать книгу.
        book_id (int): ID книги, которую нужно скачать
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    Path.mkdir(Path(folder), exist_ok=True)
    response = requests.get(url, params={"id": book_id})
    response.raise_for_status()

    if is_redirect(response):
        return

    file_path = Path(Path(folder) / f"{sanitize_filename(filename)}.txt")
    with open(file_path, "w") as file_obj:
        file_obj.write(response.text)
    return str(file_path)


def download_image(url, folder='images'):
    """Функция для скачивания картинок.
    Args:
        url (str): Cсылка на страницу книги.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """

    image_data_response = requests.get(url)
    image_data_response.raise_for_status()
    file_name = parse_file_name_from_url(url)
    file_path = Path(Path(folder) / file_name)
    Path.mkdir(Path(folder), exist_ok=True)
    if not Path(file_path).exists():
        with open(file_path, "wb") as file:
            file.write(image_data_response.content)
    return file_path


def fetch_book_data(book_id: int) -> Optional[dict]:
    """Функция для получения HTML-страницы книги.
    Args:
        book_id: ID книги.
    Returns:
        str: HTML-страница книги, если книга существует. Иначе вернет None.
    """
    try:
        url = f"https://tululu.org/b{book_id}/"
        response = requests.get(f"{url}")
        response.raise_for_status()
        if is_redirect(response):
            return
        return parse_book_page(response.content)
    except requests.exceptions.ConnectionError:
        logging.exception(f"Connection error: failed to establish connection to {url}")
        return
    except requests.exceptions.HTTPError as e:
        logging.exception(e)
        return


def download_book(book_id: int, txt_folder: str = 'books', images_folder: str = "images") -> Optional[dict]:
    book_info = fetch_book_data(book_id)
    if not book_info:
        return
    download_image(book_info.get('image_link'), images_folder)
    download_txt_url = f"https://tululu.org/txt.php"
    filename = f'{book_id}. {book_info.get("title")}'
    file_path = download_txt(url=download_txt_url, book_id=book_id, folder=txt_folder, filename=filename)
    print(f'\n\nНазвание: {book_info.get("title")}\nАвтор: {book_info.get("author")}')
    comments = book_info.get("comments")
    # if comments:
    #     print("Комментарии:")
    #     print(*comments, sep="\n")
    return update_book_info(book_info, file_path, images_folder=images_folder)


def download_books(start_id: int, end_id: int):
    for book_id in range(start_id, end_id + 1):
        download_book(book_id)
