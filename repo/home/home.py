import configparser
import logging
import os

from listening.alive import ping
from flask import Flask
from auth.ssh_endpoints import ssh_blueprint

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
from database.database import Database
from logging_manager.logger import LoggerManager

_logger = logging.getLogger(__name__)

# FLASK
app = Flask(__name__)

app.add_url_rule('/ping', view_func=ping)
app.register_blueprint(ssh_blueprint)
# END FLASK


HOME_NAME = "home"


if __name__ == '__main__':

    # Read params
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./conf/home_conf.conf"))

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

    app.config["database"] = database

    # Run flask
    app.run()



