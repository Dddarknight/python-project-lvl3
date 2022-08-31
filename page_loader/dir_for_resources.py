from page_loader.url_to_name import convert_url_to_name
import os


def create(url, dir_path):
    dir_for_resources_name = f"{convert_url_to_name(url)}_files"
    dir_for_resources_path = os.path.join(dir_path, dir_for_resources_name)
    if not os.path.exists(dir_for_resources_path):
        os.mkdir(dir_for_resources_path)
    return dir_for_resources_path
