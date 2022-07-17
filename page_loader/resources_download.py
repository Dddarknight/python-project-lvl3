import os
import re
import requests
import logging
from bs4 import BeautifulSoup
from progress.bar import ChargingBar
from page_loader.url_to_name import convert_url_to_name
from urllib.parse import urlparse


logger = logging.getLogger()


def extract_protocol(url):
    if 'https' in url:
        protocol = 'https://'
    elif 'http' in url:
        protocol = 'http://'
    else:
        protocol = 'https://'
    return protocol


def normalize_url(url, url_hostname, parent_url=None):
    if parent_url is not None:
        protocol = extract_protocol(parent_url)
    else:
        protocol = extract_protocol(url)
    if urlparse(url).scheme == '' and urlparse(url).netloc == '':
        if urlparse(url).path[0] != '/':
            url = protocol + url_hostname + '/' + url
        else:
            url = protocol + url_hostname + url
    elif urlparse(url).scheme == '':
        url = protocol[:-2] + url
    return url


def create_dir_for_resources(url, dir_path):
    dir_for_resources_name = convert_url_to_name(url) + '_files'
    dir_for_resources_path = os.path.join(dir_path, dir_for_resources_name)
    if not os.path.exists(dir_for_resources_path):
        os.mkdir(dir_for_resources_path)
    return dir_for_resources_name, dir_for_resources_path


def check_tail(tail):
    check_tail = re.findall(r"[|\W|_]", tail)
    if check_tail == []:
        tail = '.html'
    if not (check_tail == [] or check_tail == ['.']):
        tail = convert_url_to_name(tail)
    return tail


def extract_resource(link, dir_for_resources_path, url_hostname, url):
    if link.name == 'img' or link.name == 'script':
        atr = 'src'
    else:
        atr = 'href'
    _, dir_for_resources_name = os.path.split(dir_for_resources_path)
    link_internal = link.get(atr)
    normalized_url = normalize_url(link_internal, url_hostname, url)
    try:
        r = requests.get(normalized_url)
        if r.status_code != 200:
            logger.info(f'Status code {r.status_code} {link_internal}')
            return ''
        resource = r.content
        head, tail = os.path.splitext(normalized_url)
        tail = check_tail(tail)
        file_resource_name = convert_url_to_name(head)[:100] + tail
        path_abs = os.path.join(dir_for_resources_path, file_resource_name)
        with open(path_abs, 'wb') as write_file:
            write_file.write(resource)
        path_relative = os.path.join(dir_for_resources_name, file_resource_name)
        return path_relative
    except (requests.ConnectionError,
            requests.HTTPError,
            requests.URLRequired,
            requests.TooManyRedirects,
            requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema,
            requests.exceptions.InvalidURL):
        logger.debug(f'Bad request {link_internal}')


def modify_link(link, url_hostname, dir_path, url):
    if link.name == 'img' or link.name == 'script':
        atr = 'src'
    else:
        atr = 'href'
    hostname = urlparse(link.get(atr)).hostname
    if hostname is None or hostname == url_hostname:
        new_link = extract_resource(link, dir_path, url_hostname, url)
        if new_link:
            link[atr] = new_link


def resources_download(url, html_dir_path, html_file_path):
    dir_name, dir_path = create_dir_for_resources(url, html_dir_path)
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
