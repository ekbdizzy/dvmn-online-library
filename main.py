import argparse
import logging
from tululu_services.parse_services import parse_books

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser("Parse books_info from tululu.org.")
    parser.add_argument("--start_id", metavar="start_id", type=int, default=0, help="first book_id of parse list.")
    parser.add_argument("--end_id", metavar="--end_id", type=int, default=10, help="last book_id of parse list.")
    args = parser.parse_args()

    parse_books(args.start_id, args.end_id)
