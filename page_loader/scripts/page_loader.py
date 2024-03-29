#!/usr/bin/env python

from page_loader.html_page import download
from page_loader.cli import parse
from page_loader.logger import setup_logging
import sys


def main():
    logger = setup_logging()
    args = parse()
    try:
        html_path = download(args.url, output=args.output)
    except Exception as e:
        logger.error(
            f'An error occured during the execution of a program: {e}')
        sys.exit(1)
    print(f'Page was downloaded as: {html_path}')


if __name__ == '__main__':
    main()
