import logging
import os
from logging.handlers import RotatingFileHandler  # pylint: disable=C0412

LOG_NAME = "resource_calculator.log"
LOG_FOLDER = ".logs"
LOG_FILE_SIZE_MB = 5
LOG_FILE_BACKUP_COUNT = 5
# LOG_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
LOG_FORMATTER = logging.Formatter(f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")


def get_rotating_file_handler():
    log_full_path = os.path.join(LOG_FOLDER, LOG_NAME)
    os.makedirs(os.path.dirname(log_full_path), exist_ok=True)

    file_handler = RotatingFileHandler(log_full_path,
                                       maxBytes=LOG_FILE_SIZE_MB*1024*1024,
                                       backupCount=LOG_FILE_BACKUP_COUNT)
    file_handler.setFormatter(LOG_FORMATTER)
    file_handler.setLevel(logging.INFO)
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(LOG_FORMATTER)
    stream_handler.setLevel(logging.INFO)
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_rotating_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
