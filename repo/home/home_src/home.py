import configparser
import logging

from flask import Flask

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
from home_src.database.database import Database
from home_src.internet_provider.network_manager import HomeNetworkManager
from home_src.logging_manager.logger import LoggerManager

_logger = logging.getLogger(__name__)
app = Flask(__name__)


HOME_NAME = "home"

if __name__ == '__main__':

    # Read params
    config = configparser.ConfigParser()
    config.read("../home_conf.conf")

    LoggerManager(logging.getLevelName(config.get("settings", "log_level").upper()))

    HOME_NAME = config.get("settings", "home_name")

    _logger.info(f"Starting home core: {HOME_NAME}")

    database = Database(
        config.get("database", "host"),
        config.get("database", "database"),
        config.get("database", "user"),
        config.get("database", "password"),
        config.get("database", "port"),
    )

    # Network manager
    network_manager = HomeNetworkManager()

    # Run flask
    app.run()



