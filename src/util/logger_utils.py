import logging.config

_current_log = None


def get_logger():
    global _current_log
    if _current_log is None:
        _current_log = generate_logger()
    return _current_log


def generate_logger():
    logging.root.handlers = []
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    return logging.getLogger()
