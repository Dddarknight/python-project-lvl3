import os
import requests
import logging
from page_loader.resources import download as resources_download
from page_loader.url_to_name import convert_url_to_name
from page_loader.html_crawler import prepare_resources


logger = logging.getLogger()


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    logger.info(
        f'A directory for resources was created: {dir_path}')


def download(url, output=os.getcwd(), get_html=get_html):
    logger.info(f'requested url: {url}')

    file_name = convert_url_to_name(url)
    dir_for_resources_name = convert_url_to_name(url, structure='dir')

    output_path = os.path.abspath(output)
    logger.info(f'output path: {output_path}')

    html_path = os.path.join(output_path, file_name)
    logger.info(f'write html file: {html_path}')

    dir_for_resources_path = os.path.join(output_path, dir_for_resources_name)

    html = get_html(url)

    create_dir(dir_for_resources_path)

    resources, modified_html = prepare_resources(url,
                                                 dir_for_resources_path,
                                                 dir_for_resources_name,
                                                 html)
    resources_download(resources)

    with open(html_path, 'w') as html_file:
        html_file.write(modified_html)

    return html_path
