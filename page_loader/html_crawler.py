from urllib.parse import urlparse, urljoin
import os
from bs4 import BeautifulSoup
from page_loader.url_to_name import convert_url_to_name


def prepare_resources(url,
                      dir_for_resources_path,
                      dir_for_resources_name,
                      html):

    soup = BeautifulSoup(html, 'html.parser')
    tags = get_tags(soup)
    resources = get_resources(tags,
                              url,
                              dir_for_resources_path,
                              dir_for_resources_name)
    return resources, soup


def get_tags(soup):
    tags = soup.find_all('img')
    tags.extend(soup.find_all('link'))
    tags.extend(soup.find_all('script'))
    return tags


def get_resources(tags,
                  url,
                  dir_for_resources_path,
                  dir_for_resources_name):

    resources = []
    for tag in tags:
        resource = get_resource(tag,
                                url,
                                dir_for_resources_path,
                                dir_for_resources_name)
        if resource:
            resources.append(resource)
    return resources


def get_resource(tag,
                 url,
                 dir_for_resources_path,
                 dir_for_resources_name):

    attribute = get_tag_attribute(tag)
    resource_url = tag.get(attribute)
    if not resource_url:
        return None

    resource_hostname = urlparse(resource_url).netloc
    if resource_hostname and resource_hostname != urlparse(url).hostname:
        return None

    normalized_url = urljoin(f'{url}/', resource_url)

    file_resource_name = convert_url_to_name(normalized_url)
    relative_path = os.path.join(dir_for_resources_name, file_resource_name)
    absolute_path = os.path.join(dir_for_resources_path, file_resource_name)
    tag[attribute] = relative_path

    return {normalized_url: absolute_path}


def get_tag_attribute(tag):
    return 'src' if tag.name in ('img', 'script') else 'href'
