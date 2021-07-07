from pathlib import Path
import requests
from pathvalidate import sanitize_filename
import logging
from parse_services import (parse_file_name_from_url,
                            is_redirect,
                            parse_book_page)


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    Path.mkdir(Path(folder), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    if is_redirect(response):
        return

    file_path = Path(Path(folder) / f"{sanitize_filename(filename)}.txt")
    with open(file_path, "w") as file_obj:
        file_obj.write(response.text)
    return str(file_path)


def download_image(url, folder='images/'):
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


def download_books(start_id: int, end_id: int):
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
            download_image(book_info.get('image_link'))
            download_txt_url = f"https://tululu.org/text.php?id={book_id}"
            download_txt(url=download_txt_url, filename=f'{book_id}. {book_info.get("title")}')
            print(f'\n\nНазвание: {book_info.get("title")}\nАвтор: {book_info.get("author")}')
            comments = book_info.get("comments")
            if comments:
                print("Комментарии:")
                print(*comments, sep="\n")
