import argparse
import logging

from download_services import download_books

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser("Parse books_info from tululu.org.")
    parser.add_argument("--start_id", metavar="first_book_id", type=int, default=0, help="first book_id of parse list.")
    parser.add_argument("--end_id", metavar="last_book_id", type=int, default=10, help="last book_id of parse list.")
    args = parser.parse_args()

    download_books(args.start_id, args.end_id)
