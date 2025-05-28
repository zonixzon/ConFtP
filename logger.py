import logging
from datetime import datetime

class CustomFormatter(logging.Formatter):
    def format(self, record):
        dt = datetime.fromtimestamp(record.created)
        date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        msg = f"[{date_str}] local.{record.levelname}: {record.getMessage()}"
        return msg

def get_logger():
    logger = logging.getLogger('access_logger')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)
    return logger



