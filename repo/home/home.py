import configparser
import logging
import os

from listening.alive import ping
from flask import Flask
from auth.ssh_endpoints import ssh_blueprint
from network.network_gateway import network_blueprint, NetworkGateway
from flask_cors import CORS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
from database.database import Database
from logging_manager.logger import LoggerManager

_logger = logging.getLogger(__name__)

# FLASK
app = Flask(__name__)

app.add_url_rule('/ping', view_func=ping)
app.register_blueprint(ssh_blueprint)
app.register_blueprint(network_blueprint)
# END FLASK

CORS(app, origins=["http://localhost:4200"])

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
    app.config["HOME_NAME"] = HOME_NAME

    network = NetworkGateway(config, app)

    app.config["network"] = network


    # Run flask
    app.run()



