import json
import sys

import requests
from bs4 import BeautifulSoup
from urllib import parse
from download_services import download_book
from arguments_parser import get_args

if __name__ == '__main__':

    args = get_args()
    start_page, end_page = args.start_page, args.end_page
    if start_page > end_page:
        sys.exit("First page value must be less end page value.")

    all_books_info = []
    for page in range(start_page, end_page + 1):
        url = f"https://tululu.org/l55/{page}/"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")
        all_books_on_page = soup.select("table.d_book")
        print("*  " * 10, "\n", f"Page {page}", "\n", "*  " * 10, "\n")

        for book in all_books_on_page:
            book_relative_link = book.find("a")["href"]
            book_id = "".join(filter(lambda x: x.isdigit(), book_relative_link))

            book_page_url = f"https://tululu.org/b{book_id}/"
            absolute_link_book = parse.urljoin(url, book_relative_link)
            book_info = download_book(
                int(book_id),
                txt_folder='books',
                images_folder="images",
                dest_folder=args.dest_folder_path,
                skip_images=args.skip_imgs,
                skip_txt=args.skip_txt,
            )

            if book_info:
                all_books_info.append(book_info)
                print(book_page_url)

    with open(args.json_file_path, "w") as json_file_data:
        json_file_data.write(json.dumps(all_books_info, ensure_ascii=False, indent=2))
