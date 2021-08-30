## Books parser from tululu.org

Books are parsing from free online library [tululu.org](https://tululu.org).

## Before start install requirements§

~~~
pip install -r requirements.txt
~~~

## Working with project

Script `parse_tululu_category.py` has cli args:

1. `--dest_folder`: destination folder of all downloads. Default: current directory.
2. `--json_path`: destination folder of json_file with books info. Default: `./books_info.json`
3. `--skip_imgs`: skip downloading images.
4. `--skip_txt`: skip downloading txt.
5. `--start_page`: - first page number to parse.
6. `--end_page`: last page number to parse.

Usage:

~~~
python parse_tululu_category.py --dest_folder books --start_page 10 --end_page 15 --skip_imgs 
~~~

More info:

~~~
python parse_tululu_category.py -h
~~~

## Credential

Project is created as a lesson in [Devman](https://dvmn.org/modules/website-layout-for-pydev/). 


