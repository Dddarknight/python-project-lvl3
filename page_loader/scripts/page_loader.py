#!/usr/bin/env python

from page_loader.download import download
from page_loader.parsing import parsing
import logging


def main():
    logging.basicConfig(filename='page_loader.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started')
    args = parsing()
    download(
        args['http_address'], output=args['output'])
    logging.info('Finished')


if __name__ == '__main__':
    main()
