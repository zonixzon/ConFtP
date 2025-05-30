import logging
import os
from datetime import datetime

class CustomFormatter(logging.Formatter):
    pass  # Personalizzabile se necessario

def get_logger(name, level=logging.INFO):
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)  # Crea la cartella se non esiste

    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    level_name = logging.getLevelName(level).lower()
    log_filename = f"{now}_local.{level_name}.log"
    log_path = os.path.join(log_dir, log_filename)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)

        formatter = CustomFormatter(
            '[%(asctime)s] %(name)s.%(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def dimensione ():
    filepath = os.path.getsize('csv_files/cdr-wimore-2023-12-25.csv')
    return filepath

