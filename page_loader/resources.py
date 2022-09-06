import requests
import logging
from progress.bar import ChargingBar


logger = logging.getLogger()


def download(resources):
    length = len(resources)
    with ChargingBar('Downloading', max=length) as bar:
        for resource in resources:
            url = list(resource.keys())[0]
            path = resource[url]
            download_resource(url, path)
            bar.next()


def download_resource(url, absolute_path):
    response = requests.get(url)
    response.raise_for_status()
    content = response.content
    with open(absolute_path, 'wb') as write_file:
        write_file.write(content)
