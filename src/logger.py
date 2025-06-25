import logging
import os
from config import LOG_DIR

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, f"{name}.log"))
    file_handler.setFormatter(formatter)

    # Console handler (only errors)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
