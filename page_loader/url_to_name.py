from urllib.parse import urlparse
import os


def convert_url_to_name(url, structure='file'):
    hostname = urlparse(url).hostname
    path = urlparse(url).path
    root, extension = os.path.splitext(path)
    if not extension:
        extension = '.html'
    if structure == 'dir':
        extension = '_files'
    file_name = (f'{hostname}{root}').replace('/', '-').replace('.', '-')
    return f'{file_name}{extension}'
