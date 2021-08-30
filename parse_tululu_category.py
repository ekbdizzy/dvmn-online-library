import json
import sys
import requests
from bs4 import BeautifulSoup
from download_services import download_book
from arguments_parser import get_args
from parse_services import parse_books_ids

if __name__ == '__main__':

    args = get_args()
    start_page, end_page = args.start_page, args.end_page
    if start_page > end_page:
        sys.exit("First page value must be less end page value.")

    all_books_info = []
    for page in range(start_page, end_page + 1):
        print(f"\n{'* ' * 10}\nPage {page}\n{'* ' * 10}")

        url = f"https://tululu.org/l55/{page}/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        for book_id in parse_books_ids(soup):
            book_info = download_book(
                book_id,
                txt_folder='books',
                images_folder="images",
                dest_folder=args.dest_folder_path,
                skip_images=args.skip_imgs,
                skip_txt=args.skip_txt,
            )

            if book_info:
                all_books_info.append(book_info)
                print(f"https://tululu.org/b{book_id}/")

    with open(args.json_file_path, "w") as json_file_data:
        json_file_data.write(json.dumps(all_books_info, ensure_ascii=False, indent=2))
