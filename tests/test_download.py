import tempfile
import os
import requests_mock
import shutil
import pytest
from unittest import mock
import requests
from page_loader.html_page import download
import page_loader.resources as resources


def func_fake(url):
    r = 'output_text'
    return r


def test_download_fake_request():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    file_path = download(url, temp_dir.name, get_request_result=func_fake)
    with open(file_path) as read_file:
        actual = read_file.read()
        assert actual.strip() == 'output_text'


def test_download_mock():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    with requests_mock.Mocker() as mock:
        mock.get(url, text='output_text')
        download(url, temp_dir.name)
        assert mock.call_count == 1
        assert mock.request_history[0].url == url


def get_fixture_path(name):
    return os.path.join('tests/fixtures', name)


def compare(html_path, fixture_name):
    with open(html_path) as result_file:
        with open(get_fixture_path(fixture_name)) as expected_file:
            assert result_file.read() == expected_file.read()


def test_download_img(requests_mock):
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'img_download_before.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    requests_mock.get('https://ru.hexlet.io/assets/professions/nodejs.png')
    resources.download(url, dir_path, html_path)
    compare(html_path, 'img_download_after.html')
    expected_dir_name = 'ru-hexlet-io-courses_files'
    expected_dir_path = os.path.join(dir_path, expected_dir_name)
    expected_file_path = os.path.join(
        expected_dir_path, 'ru-hexlet-io-assets-professions-nodejs.png')
    assert os.path.exists(expected_dir_path)
    assert os.path.exists(expected_file_path)


def test_download_hexlet_io(requests_mock):
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'link_scr_before.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    requests_mock.get('https://ru.hexlet.io/assets/professions/nodejs.png')
    requests_mock.get('https://ru.hexlet.io/assets/application.css')
    requests_mock.get('https://ru.hexlet.io/courses')
    requests_mock.get('https://ru.hexlet.io/packs/js/runtime.js')
    resources.download(url, dir_path, html_path)
    compare(html_path, 'link_scr_after.html')
    assert len(os.listdir(dir_path)) == 2
    expected_dir_name = 'ru-hexlet-io-courses_files'
    assert len(os.listdir(
        os.path.join(dir_path, expected_dir_name))) == 4
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


def test_download_site(requests_mock):
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://site.com/blog/about'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'site-com-blog-about.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    requests_mock.get('https://site.com/blog/about')
    requests_mock.get('https://site.com/blog/about/assets/styles.css')
    requests_mock.get('https://site.com/photos/me.jpg')
    requests_mock.get('https://site.com/assets/scripts.js')
    resources.download(url, dir_path, html_path)
    assert len(os.listdir(dir_path)) == 2
    expected_dir_name = 'site-com-blog-about_files'
    assert len(os.listdir(
        os.path.join(dir_path, expected_dir_name))) == 4
    expected_dir_path = os.path.join(dir_path, expected_dir_name)
    expected_file1_path = os.path.join(
        expected_dir_path, 'site-com-blog-about.html')
    expected_file2_path = os.path.join(
        expected_dir_path, 'site-com-blog-about-assets-styles.css')
    expected_file3_path = os.path.join(
        expected_dir_path, 'site-com-photos-me.jpg')
    expected_file4_path = os.path.join(
        expected_dir_path, 'site-com-assets-scripts.js')
    assert os.path.exists(expected_dir_path)
    assert os.path.exists(expected_file1_path)
    assert os.path.exists(expected_file2_path)
    assert os.path.exists(expected_file3_path)
    assert os.path.exists(expected_file4_path)


def test_download_localhost(requests_mock):
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'http://localhost/blog/about'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    file_name = 'localhost-blog-about.html'
    shutil.copy(get_fixture_path(file_name), dir_path)
    html_path = os.path.join(dir_path, file_name)
    requests_mock.get('http://localhost/blog/about')
    requests_mock.get('http://localhost/blog/about/assets/styles.css')
    requests_mock.get('http://localhost/photos/me.jpg')
    requests_mock.get('http://localhost/assets/scripts.js')
    resources.download(url, dir_path, html_path)
    assert len(os.listdir(dir_path)) == 2
    expected_dir_name = 'localhost-blog-about_files'
    assert len(os.listdir(
        os.path.join(dir_path, expected_dir_name))) == 4
    expected_dir_path = os.path.join(dir_path, expected_dir_name)
    expected_file1_path = os.path.join(
        expected_dir_path, 'localhost-blog-about.html')
    expected_file2_path = os.path.join(
        expected_dir_path, 'localhost-blog-about-assets-styles.css')
    expected_file3_path = os.path.join(
        expected_dir_path, 'localhost-photos-me.jpg')
    expected_file4_path = os.path.join(
        expected_dir_path, 'localhost-assets-scripts.js')
    assert os.path.exists(expected_dir_path)
    assert os.path.exists(expected_file1_path)
    assert os.path.exists(expected_file2_path)
    assert os.path.exists(expected_file3_path)
    assert os.path.exists(expected_file4_path)


def test_no_dir(requests_mock):
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    fake_dir = 'fake_dir'
    dir_path = os.path.join(os.getcwd(), temp_dir.name, fake_dir)
    requests_mock.get(url)
    with pytest.raises(FileNotFoundError) as error:
        download(url, output=dir_path)
    assert error is not None


@mock.patch('os.access')
def test_no_access(mock):
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    mock.return_value = False
    with pytest.raises(PermissionError) as error:
        download(url, output=dir_path)
    assert error is not None


@pytest.mark.parametrize(
    'status_code',
    [400, 401, 402, 403, 404, 407, 408, 409, 500, 501, 502, 503, 504])
def test_http_errors(requests_mock, status_code):
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    requests_mock.get(url, status_code=status_code)
    with pytest.raises(requests.HTTPError) as error:
        download(url, output=dir_path)
    assert error is not None
