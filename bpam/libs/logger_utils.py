import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler


def get_logger(name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    logger.addHandler(RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True)))

    return logger