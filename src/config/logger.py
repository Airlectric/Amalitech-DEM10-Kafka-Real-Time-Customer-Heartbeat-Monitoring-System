import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

class ErrorTypeFilter(logging.Filter):
    def __init__(self, error_type):
        super().__init__()
        self.error_type = error_type
    def filter(self, record):
        return getattr(record, "error_type", None) == self.error_type

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    # Remove existing handlers to avoid duplicate logs
    logger.handlers = []

    # General log file
    general_handler = logging.FileHandler(os.path.join(LOG_DIR, "general.log"))
    general_handler.setLevel(LOG_LEVEL)
    general_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(general_handler)

    # Error log file
    error_handler = logging.FileHandler(os.path.join(LOG_DIR, "error.log"))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(error_handler)

    # Warning log file
    warning_handler = logging.FileHandler(os.path.join(LOG_DIR, "warning.log"))
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(warning_handler)

    # Info log file
    info_handler = logging.FileHandler(os.path.join(LOG_DIR, "info.log"))
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(info_handler)

    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOG_LEVEL)
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(stream_handler)

    return logger
