
import logging
from datetime import datetime

class CustomFormatter(logging.Formatter):
    pass  # Non serve ridefinire format se non aggiungi logica extra

def get_logger(name, level=logging.INFO):
    # Formatta il nome del file con data, ora e livello
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    level_name = logging.getLevelName(level).lower()
    log_filename = f"{now}_local.{level_name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(level)
        formatter = CustomFormatter('[%(asctime)s] local.%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

