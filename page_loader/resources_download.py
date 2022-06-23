import os
import re
import requests
from bs4 import BeautifulSoup
from page_loader.url_to_name import url_to_name
from urllib.parse import urlparse


def normalize_url(url, url_hostname):
    if urlparse(url).scheme == '' and urlparse(url).netloc == '':
        url = 'https://' + url_hostname + url
    elif urlparse(url).scheme == '':
        url = 'https:' + url
    return url


def create_dir_for_resources(url, dir_path):
    dir_for_resources_name = url_to_name(url) + '_files'
    dir_for_resources_path = os.path.join(dir_path, dir_for_resources_name)
    if not os.path.exists(dir_for_resources_path):
        os.mkdir(dir_for_resources_path)
    return dir_for_resources_name, dir_for_resources_path


def check_tail(tail):
    check_tail = re.findall(r"[|\W|_]", tail)
    if check_tail == []:
        tail = '.html'
    if not (check_tail == [] or check_tail == ['.']):
        tail = url_to_name(tail)
    return tail


def resource_extract(link, atr, dir_for_resources_path, url_hostname):
    _, dir_for_resources_name = os.path.split(dir_for_resources_path)
    link_internal = link.get(atr)
    if not link_internal:
        return link_internal
    normalized_url = normalize_url(link_internal, url_hostname)
    resource = ''
    try:
        resource = requests.get(normalized_url).content
    except Exception:
        pass
    head, tail = os.path.splitext(normalized_url)
    tail = check_tail(tail)
    file_resource_name = url_to_name(head)[:100] + tail
    path_abs = os.path.join(dir_for_resources_path, file_resource_name)
    with open(path_abs, 'wb') as write_file:
        if resource:
            write_file.write(resource)
    path_relative = os.path.join(dir_for_resources_name, file_resource_name)
    return path_relative


def in_link(link, atr, url_hostname, dir_path):
    hostname = urlparse(link.get(atr)).hostname
    if hostname is None or hostname == url_hostname:
        new_link = resource_extract(link, atr, dir_path, url_hostname)
        if new_link:
            link[atr] = new_link


def resources_download(url, html_dir_path, html_file_path):
    dir_name, dir_path = create_dir_for_resources(url, html_dir_path)
    url_hostname = urlparse(url).hostname
    with open(html_file_path) as read_file:
        soup = BeautifulSoup(read_file, 'html.parser')
    for link in soup.find_all('img'):
        in_link(link, 'src', url_hostname, dir_path)
    for link in soup.find_all('link'):
        in_link(link, 'href', url_hostname, dir_path)
    for link in soup.find_all('script'):
        in_link(link, 'src', url_hostname, dir_path)
    with open(html_file_path, 'w') as write_file:
        write_file.write(soup.prettify())
