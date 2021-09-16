import json
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape

JSON_FILE = 'books_info.json'
TEMPLATE_HTML = 'template.html'


def on_reload():
    template = env.get_template(TEMPLATE_HTML)
    rendered_page = template.render(
        books=books
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    with open(JSON_FILE) as file_data:
        books = json.loads(file_data.read())

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
