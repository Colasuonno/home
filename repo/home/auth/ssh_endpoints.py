import json

from flask import Blueprint, current_app, request, Response
import logging
import webauthn
from webauthn import options_to_json
from webauthn.helpers.structs import PublicKeyCredentialDescriptor, PublicKeyCredentialRequestOptions, \
    AuthenticationCredential
from database import LoginSSHTable


_logger = logging.getLogger(__name__)

ssh_blueprint = Blueprint('ssh_login', __name__)

@ssh_blueprint.route('/auth_options/<login>', methods=['GET'])
def ssh_login(login: str):

    login_ssh_table = current_app.config["database"].tables[LoginSSHTable.TABLE_NAME]

    # Decrypt
    public_key: str = login_ssh_table.retrieve_login_public_key(login)

    if not public_key:
        _logger.warning(f"Public key wasn't found in database table for login {login}")
        return Response("Public key wasn't found in database, for your login", mimetype='text/plain', status=401)

    login_ssh_table.users_options[login] = options_to_json(webauthn.generate_authentication_options(
        rp_id="localhost",
        allow_credentials=[
          PublicKeyCredentialDescriptor(id=public_key.encode("utf-8"))
        ]
    ))

    return Response(login_ssh_table.users_options[login], mimetype='application/json', status=200)



@ssh_blueprint.route('/auth_options/', methods=['POST'])
def verify_login():

    data = request.json

    _logger.debug("ao data")
    _logger.debug(data)

    if "login" not in data:
        _logger.warning("Login  wasn't found in request payload")
        return Response("Login wasn't found in request payload", mimetype='text/plain', status=404)

    if "credentials" not in data:
        _logger.warning("Credentials  wasn't found in request payload")
        return Response("Credentials wasn't found in request payload", mimetype='text/plain', status=404)

    login = data["login"]
    login_ssh_table = current_app.config["database"].tables[LoginSSHTable.TABLE_NAME]

    if login not in login_ssh_table.users_options:
        return Response(f"Options wasn't found inside cache for {login}", mimetype='text/plain', status=401)

    user_option = json.loads(login_ssh_table.users_options[login])

    _logger.debug("USER OPTIONS " + str(user_option))

    # Decrypt
    public_key: str = login_ssh_table.retrieve_login_public_key(login)

    if not public_key:
        _logger.warning(f"Public key wasn't found in database table for login {login}")
        return Response("Public key wasn't found in database, for your login", mimetype='text/plain', status=401)

    return Response({"success": webauthn.verify_authentication_response(
        credential=data["credentials"],
        expected_challenge=user_option["challenge"],
        expected_rp_id=user_option["rp_id"],
        credential_public_key=public_key.encode("utf-8"),
    ).user_verified}, mimetype='application/json', status=200)


