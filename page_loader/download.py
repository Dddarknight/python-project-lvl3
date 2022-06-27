import os
import requests
import logging
from page_loader.resources_download import resources_download
from page_loader.url_to_name import url_to_name


logger = logging.getLogger()


def func_request(url):
    r = requests.get(url)
    if r.status_code != 200:
        logger.info(f'Status code {r.status_code} {url}')
        raise requests.ConnectionError
    return r.text


def download(url, output=os.getcwd(), func=func_request):
    output = os.path.abspath(output)
    if not os.path.exists(output):
        logger.info('Please, print the appropriate directory')
        raise FileNotFoundError
    file_name = url_to_name(url) + '.html'
    r = func(url)
    html_path = os.path.join(output, file_name)
    with open(html_path, 'w') as write_file:
        logger.info(f'requested url: {url}')
        logger.info(f'output path: {output}')
        logger.info(f'write html file: {html_path}')
        write_file.write(r)
    resources_download(url, output, html_path)
    logger.info(f'Page was downloaded as: {html_path}')
    return html_path
