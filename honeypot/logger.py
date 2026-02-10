"""Logging helpers for the honeypot."""
import logging


def create_logger(LOG_PATH):

    # Create a custom logger
    logger = logging.getLogger("Honeypot")
    logger.setLevel(logging.INFO)

    # Create handlers: one for the file, one for the terminal (Stream)
    f_handler = logging.FileHandler(LOG_PATH)
    s_handler = logging.StreamHandler()

    # Create formatters and add them to handlers
    # This ensures your Timestamp requirement is met
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    f_handler.setFormatter(log_format)
    s_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(f_handler)
    logger.addHandler(s_handler)

    return logger