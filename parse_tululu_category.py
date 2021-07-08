import requests
from bs4 import BeautifulSoup
from urllib import parse

# first_book_link = soup.find("table", class_="d_book").find("a")["href"]
# abs_first_book_link = parse.urljoin(url, first_book_link)
# print(abs_first_book_link)

for page in range(1, 11):
    url = f"https://tululu.org/l55/{page}/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "lxml")
    all_books = soup.find_all("table", class_="d_book")
    print("*  " * 10, "\n", f"Page {page}", "\n", "*  " * 10, "\n")
    for book in all_books:
        book_link = book.find("a")["href"]
        abs_book_link = parse.urljoin(url, book_link)
        print(abs_book_link)
