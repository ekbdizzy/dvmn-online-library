from pathlib import Path
from typing import Optional
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib import parse

BOOKS_QUANTITY = 10


def fetch_book_title(book_id: int) -> Optional[str]:
    response = requests.get(f"https://tululu.org/b{book_id}/")
    response.raise_for_status()
    if not response.history:
        soup = BeautifulSoup(response.text, "lxml")
        title, _ = soup.find('h1').text.split("::")
        return title.strip()


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

    if not response.history:
        file_path = Path(Path(folder) / f"{sanitize_filename(filename)}.txt")
        with open(file_path, "w") as file_obj:
            file_obj.write(response.text)
        return str(file_path)


def parse_file_name_from_url(url):
    return parse.unquote(Path(parse.urlsplit(url).path).name)


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
    if response.history:
        return

    soup = BeautifulSoup(response.text, "lxml")
    img_link = soup.find("div", class_="bookimage").find("img")['src']
    abs_img_link = parse.urljoin("https://tululu.org", img_link)
    image_data_response = requests.get(abs_img_link)
    image_data_response.raise_for_status()

    file_name = parse_file_name_from_url(abs_img_link)
    file_path = Path(Path(folder) / file_name)
    Path.mkdir(Path(folder), exist_ok=True)
    if not Path(file_path).exists():
        with open(file_path, "wb") as file:
            file.write(image_data_response.content)
    return file_path


def main():
    for book_id in range(1, BOOKS_QUANTITY + 1):
        book_title = fetch_book_title(book_id)
        book_txt_url = f"https://tululu.org/txt.php?id={book_id}"
        download_txt(url=book_txt_url, filename=f"{book_id}. {book_title}")
        download_image(f"https://tululu.org/b{book_id}/")


if __name__ == '__main__':
    main()
