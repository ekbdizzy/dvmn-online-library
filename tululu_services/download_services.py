from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from parse_services import parse_file_name_from_url, is_redirect, parse_cover_image_link


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
    response = requests.get(url)
    response.raise_for_status()

    if is_redirect(response):
        return

    soup = BeautifulSoup(response.text, "lxml")

    img_link = parse_cover_image_link(soup)
    image_data_response = requests.get(img_link)
    image_data_response.raise_for_status()

    file_name = parse_file_name_from_url(img_link)
    file_path = Path(Path(folder) / file_name)
    Path.mkdir(Path(folder), exist_ok=True)
    if not Path(file_path).exists():
        with open(file_path, "wb") as file:
            file.write(image_data_response.content)
    return file_path


