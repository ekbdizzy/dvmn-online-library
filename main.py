import requests
from bs4 import BeautifulSoup
from urllib import parse

BOOKS_QUANTITY = 10


def parse_book_page(html: bytes) -> dict:
    """Parse title, author, image_link and genres from html."""
    soup = BeautifulSoup(html, 'lxml')
    title, author = [i.strip() for i in (soup.find('h1').text.split("::"))]
    image_link = soup.find("div", class_="bookimage").find("img")['src']
    genres = [genre.text for genre in soup.find("span", class_="d_book").find_all("a")]
    return {
        "title": title,
        "author": author,
        "image_link": parse.urljoin("https://tululu.org", image_link),
        "genres": genres,
    }


def main():
    for book_id in range(1, BOOKS_QUANTITY + 1):
        url = f"https://tululu.org/b{book_id}/"
        response = requests.get(url)
        response.raise_for_status()

        if not response.history:
            book_info = parse_book_page(response.content)
            print(book_info)


if __name__ == '__main__':
    main()
