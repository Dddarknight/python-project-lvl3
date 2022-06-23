import os
import requests
from page_loader.resources_download import resources_download
from page_loader.url_to_name import url_to_name


def func_request(url):
    r = requests.get(url)
    return r.text


def download(url, output=os.getcwd(), func=func_request):
    file_name = url_to_name(url) + '.html'
    r = func(url)
    if not os.path.exists(output):
        os.mkdir(output)
    html_path = os.path.join(output, file_name)
    with open(html_path, 'w') as write_file:
        write_file.write(r)
    resources_download(url, output, html_path)
    return html_path
