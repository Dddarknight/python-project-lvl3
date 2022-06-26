import os
import requests
import logging
import sys
from page_loader.resources_download import resources_download
from page_loader.url_to_name import url_to_name


def func_request(url):
    try:
        r = requests.get(url)
        return r.text
    except (requests.ConnectionError,
            requests.HTTPError,
            requests.URLRequired,
            requests.TooManyRedirects,
            requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema,
            requests.exceptions.InvalidURL):
        logging.exception(f'Bad request {url}')
        sys.exit(1)


def download(url, output=os.getcwd(), func=func_request):
    file_name = url_to_name(url) + '.html'
    r = func(url)
    html_path = os.path.join(output, file_name)
    try:
        with open(html_path, 'w') as write_file:
            write_file.write(r)
        resources_download(url, output, html_path)
        return html_path
    except (FileNotFoundError):
        logging.exception('Please, print the existing directory')
        sys.exit(1)
