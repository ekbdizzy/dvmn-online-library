import requests
from pathlib import Path
from typing import Optional
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib import parse


def fetch_book_title(url: str) -> Optional[str]:
    response = requests.get(url)
    response.raise_for_status()

    if response.history:
        return

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

    if response.history:
        return

    file_path = Path(Path(folder) / f"{sanitize_filename(filename)}.txt")
    with open(file_path, "w") as file_obj:
        file_obj.write(response.text)
    return str(file_path)


def parse_file_name_from_url(url: str) -> str:
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


def download_comments(url):
    response = requests.get(url)
    response.raise_for_status()

    if response.history:
        return

    soup = BeautifulSoup(response.content, "lxml")
    comments = soup.find_all("div", class_="texts")
    for comment in comments:
        print(comment.find("span", class_="black").text)


def parse_genres(url):
    response = requests.get(url)
    response.raise_for_status()

    if response.history:
        return

    soup = BeautifulSoup(response.content, "lxml")
    genres = [genre.text for genre in soup.find("span", class_="d_book").find_all("a")]
    print(genres)
