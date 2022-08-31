import logging
import sys


LOG_FILE_NAME = 'page_loader.log'


def configurate_logging():
    logging.basicConfig(filename=LOG_FILE_NAME,
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
