import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest_folder", dest='dest_folder_path', type=str, required=False,
                        help="Destination folder of all downloads")
    parser.add_argument("--json_path", dest='json_file_path', type=str, required=False,
                        default="books_info.json", help="Destination folder of json_file with books info")
    parser.add_argument("--skip_imgs", dest='skip_imgs', action='store_true', required=False,
                        default=False, help="Skip downloading images")
    parser.add_argument("--skip_txt", dest='skip_txt', action='store_true', required=False,
                        default=False, help="Skip downloading txt")
    parser.add_argument("--start_page", type=int, dest='start_page', required=False,
                        default=1, help="First page number to parse")
    parser.add_argument("--end_page", type=int, dest='end_page', required=False,
                        default=0, help="Last page number to parse")

    return parser.parse_args()
