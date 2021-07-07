from urllib import parse
from pathlib import Path
from bs4 import BeautifulSoup


def is_redirect(response) -> bool:
    if response.history:
        return True
    return False


def parse_file_name_from_url(url: str) -> str:
    return parse.unquote(Path(parse.urlsplit(url).path).name)


def parse_cover_image_link(soup: BeautifulSoup) -> str:
    image_link = soup.find("div", class_="bookimage").find("img")['src']
    return parse.urljoin("https://tululu.org", image_link)


def parse_book_page(html: bytes) -> dict:
    """Parse title, author, image_link and genres from html."""
    soup = BeautifulSoup(html, 'lxml')
    title, author = [title_and_author.strip() for title_and_author in (soup.find('h1').text.split("::"))]
    image_link = parse_cover_image_link(soup)
    genres = [genre.text for genre in soup.find("span", class_="d_book").find_all("a")]
    comments = [comment.find("span", class_="black").text for comment in soup.find_all("div", class_="texts")]
    return {
        "title": title,
        "author": author,
        "image_link": image_link,
        "genres": genres,
        "comments": comments
    }
