import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from urllib import parse
from download_services import download_txt, download_image, download_book
from parse_services import parse_book_page

PAGES = 2
all_books_info = []
for page in range(1, PAGES + 1):
    url = f"https://tululu.org/l55/{page}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "lxml")
    all_books_on_page = soup.find_all("table", class_="d_book")
    print("*  " * 10, "\n", f"Page {page}", "\n", "*  " * 10, "\n")

    for book in all_books_on_page:
        book_relative_link = book.find("a")["href"]
        book_id = "".join(filter(lambda x: x.isdigit(), book_relative_link))

        book_page_url = f"https://tululu.org/b{book_id}/"
        absolute_link_book = parse.urljoin(url, book_relative_link)
        book_info = download_book(int(book_id), txt_folder='books', images_folder="images")

        if book_info:
            all_books_info.append(book_info)
        print(book_page_url)

with open("books_info.json", "w") as json_file_data:
    json_file_data.write(json.dumps(all_books_info, ensure_ascii=False, indent=2))
