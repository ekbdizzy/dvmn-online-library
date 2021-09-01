from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from parse_services import (parse_file_name_from_url,
                            parse_book_page,
                            update_book_info, has_link_to_download_txt)


def make_folder(folder: [Path or str], dest_folder: Optional[str] = None) -> Path:
    """Создает директории dest_folder/folder или folder."""
    if dest_folder:
        Path.mkdir(Path(dest_folder), exist_ok=True)
        Path.mkdir(Path(dest_folder) / folder, exist_ok=True)
        return Path(Path(dest_folder) / folder)
    Path.mkdir(Path(folder), exist_ok=True)
    return Path(folder)


def download_txt(book_id, filename, folder: Path = Path('books'), url="https://tululu.org/txt.php"):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на страницу, с которой нужно скачать книгу.
        book_id (int): ID книги, которую нужно скачать
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """

    response = requests.get(url, params={"id": book_id})
    response.raise_for_status()

    file_path = Path(Path(folder) / f"{sanitize_filename(filename)}.txt")
    with open(file_path, "w") as file_obj:
        file_obj.write(response.text)
    return file_path


def download_image(url, folder: Path = Path('images')) -> Path:
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
    if not Path(file_path).exists():
        with open(file_path, "wb") as file:
            file.write(image_data_response.content)
    return file_path


def fetch_book_data(book_id: int) -> Optional[dict]:
    """Функция для получения HTML-страницы книги.
    Args:
        book_id: ID книги.
    Returns:
        str: Вернет словарь с информацией о книге, если ссылка на txt-файл существует. Иначе вернет None.
    """
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    if not has_link_to_download_txt(soup, book_id):
        return
    return parse_book_page(soup)


def download_book(
        book_id: int,
        txt_folder: str = 'books',
        images_folder: str = "images",
        dest_folder: Optional[str] = None,
        skip_images: bool = False,
        skip_txt: bool = False) -> Optional[dict]:
    """Функция для скачивания книги и обложки.
    Args:
        book_id: ID книги
        txt_folder: название папки для сохранения txt-файлов
        images_folder: название папки для сохранения обложек
        dest_folder: папка для сохранения всех материалов
        skip_txt: если значение True, txt-файл книги не будет загружаться
        skip_images: если значение True, обложка книги не будет загружаться
    Returns:
        dict: Информация о скачанной книге
"""
    book_info = fetch_book_data(book_id)

    if not book_info:
        return

    file_path = ''
    if not skip_txt:
        txt_folder = make_folder(txt_folder, dest_folder)
        download_txt_url = f"https://tululu.org/txt.php"
        filename = f'{book_id}. {book_info.get("title")}'
        file_path = download_txt(url=download_txt_url, book_id=book_id, folder=txt_folder, filename=filename)
        if not file_path:
            return

    if not skip_images:
        images_folder = make_folder(images_folder, dest_folder)
        download_image(book_info.get('image_link'), images_folder)

    print(f'\nНазвание: {book_info.get("title")}\nАвтор: {book_info.get("author")}')
    return update_book_info(book_info, file_path, images_folder=images_folder, skip_images=skip_images)


def download_books(start_id: int, end_id: int):
    for book_id in range(start_id, end_id + 1):
        download_book(book_id)
