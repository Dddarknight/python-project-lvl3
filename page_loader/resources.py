import os
import re
import requests
import logging
from bs4 import BeautifulSoup
from progress.bar import ChargingBar
from page_loader.url_to_name import convert_url_to_name
from urllib.parse import urlparse


MAX_FILE_NAME = 100


logger = logging.getLogger()


def extract_protocol(url):
    if 'https' in url:
        return 'https://'
    if 'http' in url:
        return 'http://'
    return 'https://'


def normalize_url(url, url_hostname, parent_url=None):
    if parent_url is not None:
        protocol = extract_protocol(parent_url)
    else:
        protocol = extract_protocol(url)
    if urlparse(url).scheme == '' and urlparse(url).netloc == '':
        if urlparse(url).path[0] != '/':
            return f"{protocol}{url_hostname}/{url}"
        return f"{protocol}{url_hostname}{url}"
    if urlparse(url).scheme == '' and url[:2] == '//':
        return f"{protocol[:-2]}{url}"
    return url


def create_dir_for_resources(url, dir_path):
    dir_for_resources_name = f"{convert_url_to_name(url)}_files"
    dir_for_resources_path = os.path.join(dir_path, dir_for_resources_name)
    if not os.path.exists(dir_for_resources_path):
        os.mkdir(dir_for_resources_path)
    return dir_for_resources_path


def check_tail(tail):
    check_tail = re.findall(r"[|\W|_]", tail)
    if check_tail == []:
        return '.html'
    if not (check_tail == [] or check_tail == ['.']):
        return re.sub(r"[\W|_]", '-', tail)
    return tail


def find_link_atr(link):
    if link.name in ('img', 'script'):
        return 'src'
    else:
        return 'href'


def extract_resource(link, dir_for_resources_path, url_hostname, url):
    tag_link = link.get(find_link_atr(link))
    _, dir_for_resources_name = os.path.split(dir_for_resources_path)
    normalized_url = normalize_url(tag_link, url_hostname, url)
    try:
        r = requests.get(normalized_url)
        if r.status_code != 200:
            logger.info(f'Status code {r.status_code} {tag_link}')
            return
        resource = r.content
        head, tail = os.path.splitext(normalized_url)
        tail = check_tail(tail)
        file_resource_name = (
            f"{convert_url_to_name(head)[:MAX_FILE_NAME]}{tail}")
        absolute_path = os.path.join(dir_for_resources_path, file_resource_name)
        with open(absolute_path, 'wb') as write_file:
            write_file.write(resource)
        relative_path = os.path.join(dir_for_resources_name, file_resource_name)
        return relative_path
    except (requests.ConnectionError,
            requests.HTTPError,
            requests.URLRequired,
            requests.TooManyRedirects,
            requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema,
            requests.exceptions.InvalidURL):
        logger.debug(f'Bad request {tag_link}')


def modify_link(link, url_hostname, dir_path, url):
    atr = find_link_atr(link)
    hostname = urlparse(link.get(atr)).hostname
    if hostname is None or hostname == url_hostname:
        new_link = extract_resource(link, dir_path, url_hostname, url)
        if new_link:
            link[atr] = new_link


def download(url, html_dir_path, html_file_path):
    dir_path = create_dir_for_resources(url, html_dir_path)
    url_hostname = urlparse(url).hostname
    with open(html_file_path) as read_file:
        soup = BeautifulSoup(read_file, 'html.parser')
        links = soup.find_all('img')
        links.extend(soup.find_all('link'))
        links.extend(soup.find_all('script'))
    length = len(links)
    with ChargingBar('Downloading', max=length) as bar:
        for i in range(0, length):
            modify_link(links[i], url_hostname, dir_path, url)
            bar.next()
    with open(html_file_path, 'w') as write_file:
        write_file.write(soup.prettify())
