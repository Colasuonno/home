import configparser
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

from home_src.database.database import Database

_logger = logging.getLogger(__name__)

HOME_NAME = "home"

if __name__ == '__main__':

    # Read params
    config = configparser.ConfigParser()
    config.read("../home_conf.conf")

    # Update logger
    logging.basicConfig(level=logging.getLevelName(config.get("settings", "log_level").upper()))
    HOME_NAME = config.get("settings", "home_name")

    _logger.info(f"Starting home core: {HOME_NAME}")

    database = Database(
        config.get("database", "host"),
        config.get("database", "database"),
        config.get("database", "user"),
        config.get("database", "password"),
        config.get("database", "port"),
    )
