import os
import requests
import logging
from progress.bar import ChargingBar
from page_loader import dir_for_resources
from page_loader.html_adaptor import prepair_resources


logger = logging.getLogger()


def download_resource(url, absolute_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content
        with open(absolute_path, 'wb') as write_file:
            write_file.write(content)
    except (requests.ConnectionError,
            requests.HTTPError,
            requests.URLRequired,
            requests.TooManyRedirects,
            requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema,
            requests.exceptions.InvalidURL):
        logger.debug(f'Bad request {url}')


def download(url, html_dir_path, html_file_path):
    dir_path = dir_for_resources.create(url, html_dir_path)
    map_urls_to_paths = prepair_resources(html_file_path, dir_path, url)
    length = len(map_urls_to_paths)
    with ChargingBar('Downloading', max=length) as bar:
        for url, path in map_urls_to_paths.items():
            download_resource(url, path)
            bar.next()
