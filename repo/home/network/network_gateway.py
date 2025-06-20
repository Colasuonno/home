import json
import os

from asn1crypto.core import Boolean
from bs4 import BeautifulSoup
from flask import Blueprint, current_app, request, Response, Config, Flask
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database.tables.system_parameter import SystemParameter

_logger = logging.getLogger(__name__)

network_blueprint = Blueprint('network', __name__)

GATEWAY_SESSION_ID_SYS_PARAMETER = "network.gateway_session_id"


class NetworkGateway:
    
    def __init__(self, config: Config, app: Flask):
        
        self.gateway, self.login_network, self.login_password = config.get("network", "gateway"), config.get("network",
                                                                                              "login"), config.get("network", "password")
        self.database = app.config["database"]

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.login(app)






    def retrieve_session_id(self, app):
        with self.database.obtain_cursor() as cursor:
            return self.database.fetchall(cursor, app.config["database"].tables[SystemParameter.TABLE_NAME].get_by_id(GATEWAY_SESSION_ID_SYS_PARAMETER))[0][0]

    def login(self, app) -> str | None:
        """Effettua il login e restituisce il session ID dal cookie."""
        login_url = f"{self.gateway}/login.lp"

        self.driver.get(login_url)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        # Inserisce username e password
        self.driver.find_element(By.NAME, "password").send_keys(self.login_password)
        self.driver.find_element(By.CSS_SELECTOR, "input[type='button']").click()

        WebDriverWait(self.driver, 10).until(
            lambda d: "login.lp" not in d.current_url
        )

        session_cookie = None
        for cookie in self.driver.get_cookies():
            if cookie['name'] == 'xAuth_SESSION_ID':
                session_cookie = cookie['value']
                break

        if not session_cookie:
            _logger.error("Login Failed: cookie not found for network gateway.")
            return

        _logger.info("Modem Login Successful!")

        # Salva nel database
        with app.app_context():
            with self.database.obtain_cursor() as cursor:
                self.database.execute(cursor,
                                      current_app.config["database"].tables[
                                          SystemParameter.TABLE_NAME].insert(
                                          GATEWAY_SESSION_ID_SYS_PARAMETER, session_cookie
                                      ), silent=True
                                      )



@network_blueprint.route('/network/clients', methods=['GET'])
def clients():
    network = current_app.config["network"]
    session_id = network.retrieve_session_id(current_app)

    _logger.info("Sessione iniziale: " + str(session_id))

    if not session_id:
        network.login(current_app)
        session_id = network.retrieve_session_id(current_app)

    if not session_id:
        return Response("Login Failed", mimetype='text/plain', status=401)

    _logger.info(f"Session ID: {session_id}")

    driver = network.driver
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(f"{network.gateway}/devices.lp")

        # Attendi che almeno una lista venga caricata (Ethernet, per esempio)
        wait.until(EC.presence_of_element_located((By.ID, "sEthernetList")))

        device_list = {
            'ethernet': [],
            'wifi': [],
            'fxs': [],
            'usb': [],
        }

        # Ethernet
        try:
            ethernet_items = driver.find_elements(By.CSS_SELECTOR, "#sEthernetList li.device")
            for li in ethernet_items:
                device_list['ethernet'].append({
                    "name": li.get_attribute("name"),
                    "ip": li.get_attribute("data-id"),
                    "mac": li.get_attribute("mac-id"),
                })
        except:
            pass

        # WiFi
        try:
            wifi_items = driver.find_elements(By.CSS_SELECTOR, "#sWifimergeList li.device")
            for li in wifi_items:
                spans = li.find_elements(By.CLASS_NAME, "device-subinfo")
                mac = spans[0].text.strip() if len(spans) > 0 else ""
                band = spans[1].text.strip() if len(spans) > 1 else ""
                ip = spans[2].text.strip() if len(spans) > 2 else ""
                device_list['wifi'].append({
                    "name": li.get_attribute("name"),
                    "ip": ip,
                    "mac": mac,
                    "band": band,
                })
        except:
            pass

        # FXS
        try:
            fxs_items = driver.find_elements(By.CSS_SELECTOR, "#sFxsList li.device")
            for li in fxs_items:
                name = li.get_attribute("name")
                number_span = li.find_element(By.CLASS_NAME, "device-subinfo")
                device_list['fxs'].append({
                    "name": name,
                    "number": number_span.text.strip() if number_span else ""
                })
        except:
            pass

        # USB (se presente)
        device_list['usb'] = []

        _logger.info(device_list)
        return Response(json.dumps(device_list), mimetype='application/json', status=200)

    except Exception as e:
        _logger.error(e)
        return Response("Errore durante l'accesso alla pagina", mimetype='text/plain', status=500)

