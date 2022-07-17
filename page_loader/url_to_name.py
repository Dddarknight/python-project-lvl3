import re


def convert_url_to_name(url):
    url_without_http = re.findall('(?<=https://).*|(?<=http://).*', url)
    file_name = re.sub(r"[\W|_]", '-', url_without_http[0])
    return file_name
