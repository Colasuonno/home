import base64
import json
import time
from datetime import datetime
from flask import Blueprint, current_app, Response, request
import logging
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from database import LoginSSHTable

_logger = logging.getLogger(__name__)

ssh_blueprint = Blueprint('ssh_login', __name__)

# Mak skew 10 seconds
MAX_SKEW = 10

def verify_request_signature(data: dict) -> Response:
    """
    Auth a specific client given data from HTTP request
    The idea is to get the cleartext from "timestamp" and compare with
     encrypted "signature" with the public key given
    from "profile"
    :param data: the json payload of the HTTP request
    :return: True if auth
    """
    if "timestamp" not in data or type(data["timestamp"]) is not int:
        _logger.warning(f"Timestamp wasn't found in request payload or is invalid {data["timestamp"] if "timestamp" in data else None}")
        return Response("Timestamp wasn't found in request payload",mimetype='text/plain', status=404)

    if "login" not in data:
        _logger.warning("Login wasn't found in request payload")
        return Response("Login wasn't found in request payload",mimetype='text/plain', status=404)

    if "signature" not in data:
        _logger.warning("Signature wasn't found in request payload")
        return Response("Signature wasn't found in request payload",mimetype='text/plain', status=404)

    login_ssh_table = current_app.config["database"].tables[LoginSSHTable.TABLE_NAME]

    # Decrypt
    public_key = login_ssh_table.retrieve_login_public_key(data["login"])

    if not public_key:
        _logger.warning(f"Public key wasn't found in database table for login {data["login"]}")
        return Response("Public key wasn't found in database, for your login",mimetype='text/plain', status=401)

    # Check for timestamp validity
    now = int(time.time())
    timestamp = int(data["timestamp"])

    _logger.info(f"Timestamp was: {now}")

    if now - timestamp >= MAX_SKEW:
        _logger.warning(f"Timestamp was too old from {data["login"]} actually {(now-timestamp)} seconds")
        return Response("Timestamp is too old, retry", mimetype='text/plain', status=401)

    # Validate signature
    public_key = serialization.load_pem_public_key(public_key.encode())

    try:
        public_key.verify(
            base64.b64decode(data["signature"]),
            str(data["timestamp"]).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return Response("Access Gained", mimetype='text/plain', status=200)
    except Exception as e:
        _logger.warning(f"Login failed from {data["login"]}")
        _logger.error(e)
        return Response("Access Denied", mimetype='text/plain', status=401)

@ssh_blueprint.route('/ssh_login/', methods=['POST'])
def ssh_login():
    return verify_request_signature(request.json)

