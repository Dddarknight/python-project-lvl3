import os
import requests
import logging
import sys
from page_loader.resources_download import resources_download
from page_loader.url_to_name import url_to_name


logger = logging.getLogger()


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
        logger.debug(f'Bad request {url}')
        sys.exit(1)


def download(url, output=os.getcwd(), func=func_request):
    output = os.path.abspath(output)
    file_name = url_to_name(url) + '.html'
    r = func(url)
    html_path = os.path.join(output, file_name)
    try:
        with open(html_path, 'w') as write_file:
            logger.info(f'requested url: {url}')
            logger.info(f'output path: {output}')
            logger.info(f'write html file: {html_path}')
            write_file.write(r)
        resources_download(url, output, html_path)
        logger.info(f'Page was downloaded as: {html_path}')
        return html_path
    except (FileNotFoundError, PermissionError):
        logger.info('Please, print the appropriate directory')
        sys.exit(1)
