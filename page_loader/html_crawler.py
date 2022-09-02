from urllib.parse import urlparse, urljoin
import os
import re
from page_loader.url_to_name import convert_url_to_name


MAX_FILE_NAME = 100


def prepair_resources(url,
                      dir_for_resources_path,
                      dir_for_resources_name,
                      soup):

    tags = get_tags(soup)
    url_hostname = urlparse(url).hostname
    map_urls_to_paths = modify_tags(
        tags, url_hostname, dir_for_resources_path, dir_for_resources_name)
    return map_urls_to_paths


def get_tags(soup):
    tags = soup.find_all('img')
    tags.extend(soup.find_all('link'))
    tags.extend(soup.find_all('script'))
    return tags


def modify_tags(tags,
                url_hostname,
                dir_for_resources_path,
                dir_for_resources_name):

    resources = {}
    for tag in tags:
        resource = modify_tag(
            tag, url_hostname, dir_for_resources_path, dir_for_resources_name)
        if resource:
            resources.update(resource)
    return resources


def modify_tag(tag,
               url_hostname,
               dir_for_resources_path,
               dir_for_resources_name):

    attribute = get_tag_attribute(tag)
    tag_link = tag.get(get_tag_attribute(tag))
    if not tag_link:
        return None

    hostname = urlparse(tag.get(attribute)).netloc
    if hostname and hostname != url_hostname:
        return None

    base_url = f'https://{url_hostname}/'
    normalized_url = urljoin(base_url, urlparse(tag_link).path)

    file_resource_name = make_file_resource_name(normalized_url)
    relative_path = os.path.join(dir_for_resources_name, file_resource_name)
    absolute_path = os.path.join(dir_for_resources_path, file_resource_name)
    tag[attribute] = relative_path

    return {normalized_url: absolute_path}


def make_file_resource_name(normalized_url):
    head, tail = os.path.splitext(normalized_url)
    checked_tail = check_tail(tail)
    return f"{convert_url_to_name(head)[:MAX_FILE_NAME]}{checked_tail}"


def get_tag_attribute(tag):
    if tag.name in ('img', 'script'):
        return 'src'
    return 'href'


def check_tail(tail):
    check_tail = re.findall(r"[|\W|_]", tail)
    if check_tail == []:
        return '.html'
    if not (check_tail == [] or check_tail == ['.']):
        return re.sub(r"[\W|_]", '-', tail)
    return tail
