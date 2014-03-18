# this module was more useful before I added rainbow to django

import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    return logger