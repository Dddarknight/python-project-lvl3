import argparse


def parsing():
    parser = argparse.ArgumentParser(
        description='Download page and save to mentioned directory')
    parser.add_argument('http_address')
    parser.add_argument('-o', '--output')
    args = vars(parser.parse_args())
    return args
