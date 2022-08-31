from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import re
from page_loader.url_to_name import convert_url_to_name


MAX_FILE_NAME = 100


def prepair_resources(html_file_path, dir_path, url):
    with open(html_file_path) as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    links = prepair_links(soup)
    url_hostname = urlparse(url).hostname
    map_urls_to_paths = modify_links(links, url_hostname, dir_path, url)
    change_html_file(html_file_path, soup)
    return map_urls_to_paths


def prepair_links(soup):
    links = soup.find_all('img')
    links.extend(soup.find_all('link'))
    links.extend(soup.find_all('script'))
    return links


def modify_links(links, url_hostname, dir_path, url):
    map_urls_to_paths = {}
    for link in links:
        map_url_to_path = modify_link(link, url_hostname, dir_path, url)
        if map_url_to_path:
            map_urls_to_paths.update(map_url_to_path)
    return map_urls_to_paths


def modify_link(link, url_hostname, dir_path, url):
    atr = find_link_atr(link)
    hostname = urlparse(link.get(atr)).hostname
    if not (hostname is None or hostname == url_hostname):
        return None
    tag_link = link.get(find_link_atr(link))
    if not tag_link:
        return None
    normalized_url = normalize_url(tag_link, url_hostname, url)
    _, dir_for_resources_name = os.path.split(dir_path)
    file_resource_name = make_file_resource_name(normalized_url)
    relative_path = os.path.join(dir_for_resources_name, file_resource_name)
    if relative_path:
        link[atr] = relative_path
    absolute_path = os.path.join(dir_path, file_resource_name)
    return {normalized_url: absolute_path}


def change_html_file(html_file_path, soup):
    with open(html_file_path, 'w') as html_file:
        html_file.write(soup.prettify())


def make_file_resource_name(normalized_url):
    head, tail = os.path.splitext(normalized_url)
    checked_tail = check_tail(tail)
    return f"{convert_url_to_name(head)[:MAX_FILE_NAME]}{checked_tail}"


def find_link_atr(link):
    if link.name in ('img', 'script'):
        return 'src'
    return 'href'


def extract_protocol(url):
    if 'https' in url:
        return 'https://'
    if 'http' in url:
        return 'http://'
    return 'https://'


def normalize_url(url, url_hostname, parent_url=None):
    protocol = extract_protocol(
        parent_url) if parent_url is not None else extract_protocol(url)
    if urlparse(url).scheme == '' and urlparse(url).netloc == '':
        if urlparse(url).path[0] != '/':
            return f"{protocol}{url_hostname}/{url}"
        return f"{protocol}{url_hostname}{url}"
    if urlparse(url).scheme == '' and url[:2] == '//':
        return f"{protocol[:-2]}{url}"
    return url


def check_tail(tail):
    check_tail = re.findall(r"[|\W|_]", tail)
    if check_tail == []:
        return '.html'
    if not (check_tail == [] or check_tail == ['.']):
        return re.sub(r"[\W|_]", '-', tail)
    return tail
