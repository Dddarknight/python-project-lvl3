import requests
import logging
from progress.bar import ChargingBar
from page_loader.html_crawler import prepair_resources


logger = logging.getLogger()


def crawling_and_download(url,
                          dir_for_resources_path,
                          dir_for_resources_name,
                          soup):
    map_urls_to_paths = prepair_resources(url,
                                          dir_for_resources_path,
                                          dir_for_resources_name,
                                          soup)
    download(map_urls_to_paths)


def download(map_urls_to_paths):
    length = len(map_urls_to_paths)
    with ChargingBar('Downloading', max=length) as bar:
        for url, path in map_urls_to_paths.items():
            download_resource(url, path)
            bar.next()


def download_resource(url, absolute_path):
    response = requests.get(url)
    response.raise_for_status()
    content = response.content
    with open(absolute_path, 'wb') as write_file:
        write_file.write(content)
