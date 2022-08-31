#!/usr/bin/env python

from page_loader.html_page import download
from page_loader.cli import parse
from page_loader.log_config import configurate_logging


def main():
    configurate_logging()
    args = parse()
    html_path = download(
        args.url, output=args.output)
    print(f'Page was downloaded as: {html_path}')


if __name__ == '__main__':
    main()
