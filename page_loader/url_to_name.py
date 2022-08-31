import re


def convert_url_to_name(url):
    url_without_http = re.findall('(?<=https://).*|(?<=http://).*', url)
    modified_url = url_without_http[0] if url_without_http else url
    file_name = re.sub(r"[\W|_]", '-', modified_url)
    return file_name
