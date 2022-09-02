import os
import requests
import logging
from bs4 import BeautifulSoup
import page_loader.resources as resources
from page_loader.url_to_name import convert_url_to_name


logger = logging.getLogger()


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def create_dir(dir_for_resources_path):
    if not os.path.exists(dir_for_resources_path):
        os.mkdir(dir_for_resources_path)
    logger.info(
        f'A directory for resources was created: {dir_for_resources_path}')
    return dir_for_resources_path


def download(url, output=os.getcwd(), get_html=get_html):
    logger.info(f'requested url: {url}')

    file_name = f"{convert_url_to_name(url)}.html"

    output_path = os.path.abspath(output)
    logger.info(f'output path: {output_path}')

    html_path = os.path.join(output_path, file_name)
    logger.info(f'write html file: {html_path}')

    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    dir_for_resources_name = f"{convert_url_to_name(url)}_files"
    dir_for_resources_path = create_dir(
        os.path.join(output_path, dir_for_resources_name))

    resources.crawling_and_download(url,
                                    dir_for_resources_path,
                                    dir_for_resources_name,
                                    soup)

    with open(html_path, 'w') as html_file:
        html_file.write(soup.prettify())

    return html_path
