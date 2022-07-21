import tempfile
import os
import requests_mock
import shutil
import logging
import pytest
import pook
import requests
from page_loader.html_page import download
import page_loader.resources as resources


logging.basicConfig(filename='page_loader.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


def func_fake(address):
    r = 'output_text'
    return r


def test_download_fake_request(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    file_path = download(url, temp_dir.name, get_request_result=func_fake)
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


@pook.on
def test_download_img(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'img_download_before.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    pook.get('https://ru.hexlet.io/assets/professions/nodejs.png', reply=200)
    resources.download(url, dir_path, html_path)
    with open(html_path) as result_file:
        with open(
                get_fixture_path('img_download_after.html')) as expected_file:
            assert result_file.read() == expected_file.read()
    expected_dir_name = 'ru-hexlet-io-courses_files'
    expected_dir_path = os.path.join(dir_path, expected_dir_name)
    expected_file_path = os.path.join(
        expected_dir_path, 'ru-hexlet-io-assets-professions-nodejs.png')
    assert os.path.exists(expected_dir_path)
    assert os.path.exists(expected_file_path)


@pook.on
def test_download_res(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'link_scr_before.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    pook.get('https://ru.hexlet.io/assets/professions/nodejs.png', reply=200)
    pook.get('https://ru.hexlet.io/assets/application.css', reply=200)
    pook.get('https://ru.hexlet.io/courses', reply=200)
    pook.get('https://ru.hexlet.io/packs/js/runtime.js', reply=200)
    resources.download(url, dir_path, html_path)
    with open(html_path) as result_file:
        with open(get_fixture_path('link_scr_after.html')) as expected_file:
            assert result_file.read() == expected_file.read()
    expected_dir_name = 'ru-hexlet-io-courses_files'
    expected_dir_path = os.path.join(dir_path, expected_dir_name)
    expected_file1_path = os.path.join(
        expected_dir_path, 'ru-hexlet-io-assets-application.css')
    expected_file2_path = os.path.join(
        expected_dir_path, 'ru-hexlet-io-assets-professions-nodejs.png')
    expected_file3_path = os.path.join(
        expected_dir_path, 'ru-hexlet-io-packs-js-runtime.js')
    assert os.path.exists(expected_dir_path)
    assert os.path.exists(expected_file1_path)
    assert os.path.exists(expected_file2_path)
    assert os.path.exists(expected_file3_path)


@pook.on
def test_download_res2(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://site.com/blog/about'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'site-com-blog-about.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    pook.get('https://site.com/blog/about', reply=200)
    pook.get('https://site.com/blog/about/assets/styles.css', reply=200)
    pook.get('https://site.com/photos/me.jpg', reply=200)
    pook.get('https://site.com/assets/scripts.js', reply=200)
    resources.download(url, dir_path, html_path)
    assert len(os.listdir(dir_path)) == 2
    assert len(os.listdir(os.path.join(dir_path, 'site-com-blog-about_files'))) == 4


@pook.on
def test_download_res3(caplog):
    logger.debug('test')
    caplog.set_level(logging.DEBUG)
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'http://localhost/blog/about'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'localhost-blog-about.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    pook.get('http://localhost/blog/about', reply=200)
    pook.get('http://localhost/blog/about/assets/styles.css', reply=200)
    pook.get('http://localhost/photos/me.jpg', reply=200)
    pook.get('http://localhost/assets/scripts.js', reply=200)
    resources.download(url, dir_path, html_path)
    assert len(os.listdir(dir_path)) == 2
    assert len(os.listdir(os.path.join(dir_path, 'localhost-blog-about_files'))) == 4


@pook.on
def test_no_dir():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    fake_dir = 'fake_dir'
    dir_path = os.path.join(os.getcwd(), temp_dir.name, fake_dir)
    pook.get(url, reply=200)
    with pytest.raises(FileNotFoundError) as e:
        download(url, output=dir_path)
    assert e is not None


@pook.on
def test_invalid_url():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.ix'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    pook.get(url, reply=404)
    with pytest.raises(requests.ConnectionError) as e:
        download(url, output=dir_path)
    assert e is not None
