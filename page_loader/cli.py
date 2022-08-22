import argparse


def parse():
    parser = argparse.ArgumentParser(
        description='Download page and save to mentioned directory')
    parser.add_argument('url')
    parser.add_argument('-o', '--output')
    return parser.parse_args()
