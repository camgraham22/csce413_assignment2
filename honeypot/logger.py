"""Logging helpers for the honeypot."""
import logging


def create_logger(LOG_PATH):

    logger = logging.getLogger("Honeypot")
    logger.setLevel(logging.INFO)

    f_handler = logging.FileHandler(LOG_PATH)
    s_handler = logging.StreamHandler()

    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    f_handler.setFormatter(log_format)
    s_handler.setFormatter(log_format)

    logger.addHandler(f_handler)
    logger.addHandler(s_handler)

    return logger