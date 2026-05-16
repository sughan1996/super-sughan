import logging

from app.config import log_level

def setup_logger(name):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(log_level)
    logger.propagate = False
    formatter = logging.Formatter(
        "%(filename)s:%(lineno)d - %(funcName)s() | %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logger("super-sughan")

if __name__ == "__main__":
    logger.info("Logger initialized")

