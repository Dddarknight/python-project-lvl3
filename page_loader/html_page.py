import os
import requests
import logging
import page_loader.resources as resources
from page_loader.url_to_name import convert_url_to_name


logger = logging.getLogger()


def get_request_result(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def check_output(output_path):
    if not os.path.exists(output_path):
        logger.info('Please, print the appropriate directory')
        raise FileNotFoundError
    if not os.access(output_path, os.W_OK):
        logger.info('Access denied')
        raise PermissionError


def download(url, output=os.getcwd(), get_request_result=get_request_result):
    logger.info(f'requested url: {url}')
    file_name = f"{convert_url_to_name(url)}.html"
    output_path = os.path.abspath(output)
    check_output(output_path)
    logger.info(f'output path: {output_path}')
    html_path = os.path.join(output_path, file_name)
    logger.info(f'write html file: {html_path}')
    html = get_request_result(url)
    with open(html_path, 'w') as html_file:
       html_file.write(html)
    resources.download(url, output, html_path)
    return html_path
