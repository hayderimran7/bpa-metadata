import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True)))

    return logger