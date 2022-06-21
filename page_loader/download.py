import os
import re
import requests


def func_request(url):
    r = requests.get(url)
    return r.text


def download(url, output=os.getcwd(), func=func_request):
    url_without_http = re.findall('[^https://|http://].*', url)
    file_name = re.sub(r"[\W|_]", '-', url_without_http[0]) + '.html'
    r = func(url)
    if not os.path.exists(output):
        os.mkdir(output)
    new_url = os.path.join(output, file_name)
    with open(new_url, 'w') as write_file:
        write_file.write(r)
    return new_url
