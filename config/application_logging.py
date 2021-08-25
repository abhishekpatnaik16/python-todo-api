import logging

__handler = logging.StreamHandler()
__formatter = logging.Formatter(
    fmt = '%(levelname)s(%(name)s):\t%(message)s'
)
__handler.formatter = __formatter


def get_app_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.addHandler(__handler)
    return logger
