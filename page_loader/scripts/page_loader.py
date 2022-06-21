#!/usr/bin/env python

from page_loader.download import download
from page_loader.parsing import parsing


def main():
    args = parsing()
    download(
        args['http_address'], output=args['output'])


if __name__ == '__main__':
    main()
