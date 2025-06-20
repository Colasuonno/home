import logging
import os
from datetime import datetime
from logging import CRITICAL
from logging.handlers import RotatingFileHandler

_logger = logging.getLogger(__name__)

LOGS_PATH = "logs"

class LoggerManager:

    def __init__(self, level=logging.INFO):

        if not os.path.exists(LOGS_PATH):
            os.makedirs(LOGS_PATH)

        log_file = os.path.join(LOGS_PATH, f'home_{datetime.now().strftime("%Y-%m-%d")}.log')


        # Configura il logger con un file rotante
        handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024,
                                      backupCount=3)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        logger = logging.getLogger()
        logger.addHandler(handler)

        logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(CRITICAL)
        logging.getLogger("urllib3.connectionpool").setLevel(CRITICAL)