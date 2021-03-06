import os
import requests
import logging
import page_loader.resources as resources
from page_loader.url_to_name import convert_url_to_name


logger = logging.getLogger()


def get_request_result(url):
    r = requests.get(url)
    if r.status_code != 200:
        logger.info(f'Status code {r.status_code} {url}')
        raise requests.ConnectionError
    return r.text


def download(url, output=os.getcwd(), get_request_result=get_request_result):
    output = os.path.abspath(output)
    if not os.path.exists(output):
        logger.info('Please, print the appropriate directory')
        raise FileNotFoundError
    file_name = convert_url_to_name(url) + '.html'
    r = get_request_result(url)
    html_path = os.path.join(output, file_name)
    with open(html_path, 'w') as write_file:
        logger.info(f'requested url: {url}')
        logger.info(f'output path: {output}')
        logger.info(f'write html file: {html_path}')
        write_file.write(r)
    resources.download(url, output, html_path)
    logger.info(f'Page was downloaded as: {html_path}')
    return html_path
