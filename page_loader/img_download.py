import os
import requests
from bs4 import BeautifulSoup
from page_loader.url_to_name import url_to_name
from urllib.parse import urlparse


def normalize_img_url(image_url, url_hostname):
    if urlparse(image_url).scheme == '' and urlparse(image_url).netloc == '':
        image_url = 'https://' + url_hostname + image_url
    elif urlparse(image_url).scheme == '':
        image_url = 'https:' + image_url
    return image_url


def img_download(url, dir_path, html_path):
    dir_for_img_name = url_to_name(url) + '_files'
    url_hostname = urlparse(url).hostname
    dir_for_img_path = os.path.join(dir_path, dir_for_img_name)
    if not os.path.exists(dir_for_img_path):
        os.mkdir(dir_for_img_path)
    with open(html_path) as read_file:
        soup = BeautifulSoup(read_file, 'html.parser')
    for link in soup.find_all('img'):
        image_url = link.get('src')
        image_url = normalize_img_url(image_url, url_hostname)
        image = requests.get(image_url).content
        head, tail = os.path.splitext(image_url)
        image_name = url_to_name(head) + tail
        image_path_abs = os.path.join(dir_for_img_path, image_name)
        with open(image_path_abs, 'wb') as write_file:
            write_file.write(image)
        image_path_relative = os.path.join(dir_for_img_name, image_name)
        link['src'] = image_path_relative
    with open(html_path, 'w') as write_file:
        write_file.write(soup.prettify())
