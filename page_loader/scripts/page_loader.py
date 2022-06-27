#!/usr/bin/env python

from page_loader.download import download
from page_loader.parsing import parsing
import logging
import sys


def main():
    logging.basicConfig(filename='page_loader.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger()
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    file_handler = logging.FileHandler(filename='page_loader.log')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    args = parsing()
    download(
        args['http_address'], output=args['output'])


if __name__ == '__main__':
    main()
