import tempfile
import os
import requests_mock
import shutil
import logging
import pytest
from page_loader.download import download
from page_loader.resources_download import resources_download
from page_loader.url_to_name import url_to_name


logger = logging.getLogger(__name__)


def func_fake(address):
    r = 'output_text'
    return r


def test_download_fake_request(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    file_path = download(url, temp_dir.name, func=func_fake)
    with open(file_path) as read_file:
        actual = read_file.read()
        assert actual.strip() == 'output_text'


def test_download_mock(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    with requests_mock.Mocker() as mock:
        mock.get(url, text='output_text')
        download(url, temp_dir.name)
        assert mock.call_count == 1
        assert mock.request_history[0].url == url


def get_fixture_path(name):
    return os.path.join('tests/fixtures', name)


def test_download_img(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'img_download_before.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    resources_download(url, dir_path, html_path)
    with open(html_path) as result_file:
        with open(get_fixture_path('img_download_after.html')) as expected_file:
            assert result_file.read() == expected_file.read()
    expected_dir_name = 'ru-hexlet-io-courses_files'
    expected_dir_path = os.path.join(dir_path, expected_dir_name)
    expected_file_path = os.path.join(expected_dir_path, 'ru-hexlet-io-assets-professions-nodejs.png')
    assert os.path.exists(expected_dir_path)
    assert os.path.exists(expected_file_path)


def test_download_res(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'link_scr_before.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    resources_download(url, dir_path, html_path)
    with open(html_path) as result_file:
        with open(get_fixture_path('link_scr_after.html')) as expected_file:
            assert result_file.read() == expected_file.read()
    expected_dir_name = 'ru-hexlet-io-courses_files'
    expected_dir_path = os.path.join(dir_path, expected_dir_name)
    expected_file1_path = os.path.join(expected_dir_path, 'ru-hexlet-io-assets-application.css')
    expected_file2_path = os.path.join(expected_dir_path, 'ru-hexlet-io-assets-professions-nodejs.png')
    expected_file3_path = os.path.join(expected_dir_path, 'ru-hexlet-io-packs-js-runtime.js')
    assert os.path.exists(expected_dir_path)
    assert os.path.exists(expected_file1_path)
    assert os.path.exists(expected_file2_path)
    assert os.path.exists(expected_file3_path)
