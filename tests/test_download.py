import tempfile
import os
import requests_mock
import pytest
import requests
from page_loader import download


def get_fixture_path(name):
    return os.path.join('tests/fixtures', name)


def compare(html_path, fixture_name):
    with open(html_path) as result_file:
        with open(get_fixture_path(fixture_name)) as expected_file:
            assert result_file.read() == expected_file.read()


def func_fake(url):
    response = 'output_text'
    return response


def test_download_fake_request():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    file_path = download(url, temp_dir.name, get_html=func_fake)
    with open(file_path) as read_file:
        actual = read_file.read()
        assert actual.strip() == 'output_text'


def test_download_with_url_and_https():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    output_path = os.path.join(os.getcwd(), temp_dir.name)

    with open(get_fixture_path('link_src_before.html')) as html_file:
        html = html_file.read()

    url = 'https://ru.hexlet.io/courses'
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, text=html)
        html_path = download(url, output_path)

    compare(html_path, 'link_src_after.html')

    assert len(os.listdir(output_path)) == 2
    expected_dir_name = 'ru-hexlet-io-courses_files'
    assert len(os.listdir(
        os.path.join(output_path, expected_dir_name))) == 4

    expected_dir_path = os.path.join(output_path, expected_dir_name)
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


def test_download_with_localhost_and_http():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    output_path = os.path.join(os.getcwd(), temp_dir.name)

    with open(get_fixture_path('localhost-blog-about.html')) as html_file:
        html = html_file.read()

    url = 'http://localhost/blog/about'
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, text=html)
        html_path = download(url, output_path)

    compare(html_path, 'expected/localhost-blog-about.html')

    assert len(os.listdir(output_path)) == 2
    expected_dir_name = 'localhost-blog-about_files'
    assert len(os.listdir(
        os.path.join(output_path, expected_dir_name))) == 4

    expected_dir_path = os.path.join(output_path, expected_dir_name)
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


def test_no_access():
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io/courses'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    os.chmod(dir_path, 444)
    with pytest.raises(PermissionError):
        download(url, output=dir_path)


@pytest.mark.parametrize(
    'status_code',
    [400, 401, 402, 403, 404, 407, 408, 409, 500, 501, 502, 503, 504])
def test_http_errors(requests_mock, status_code):
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    url = 'https://ru.hexlet.io'
    dir_path = os.path.join(os.getcwd(), temp_dir.name)
    requests_mock.get(url, status_code=status_code)
    with pytest.raises(requests.HTTPError):
        download(url, output=dir_path)
