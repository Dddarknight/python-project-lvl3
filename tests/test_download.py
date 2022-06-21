from page_loader.download import download
import tempfile
import os
import requests_mock


def func_fake(address):
    r = 'output_text'
    return r


def test_download_fake_request():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    file_path = download(url, temp_dir.name, func=func_fake)
    with open(file_path) as read_file:
        assert read_file.read() == 'output_text'


def test_download_mock():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    with requests_mock.Mocker() as mock:
        mock.get(url, text='output_text')
        download(url, temp_dir.name)
        assert mock.call_count == 1
        assert mock.request_history[0].url == url
