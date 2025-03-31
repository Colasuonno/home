import logging
import psutil
import socket

_logger = logging.getLogger(__name__)

class HomeNetworkManager:

    def __init__(self):
        self.network_connections = []
        self.load_connections()

    def load_connections(self):

        self.network_connections.clear()
        _logger.info("Loading network connections...")

        # Visualize current network manager and store it
        interfaces = psutil.net_if_addrs()
        connections = psutil.net_if_stats()

        for interface, addresses in interfaces.items():

            # Skip down interface
            if not connections[interface].isup:
                continue

            interface_info = {
                "interface": interface,
                "addresses": []
            }

            for addr in addresses:

                address_info = {
                    "address": addr.address,
                }

                if addr.family == socket.AF_INET:
                    address_info["family"] = "IPv4"
                elif addr.family == socket.AF_INET6:
                    address_info["family"] = "IPv6"
                elif addr.family == psutil.AF_LINK:
                    address_info["family"] = "MAC"


                interface_info["addresses"].append(address_info)


            self.network_connections.append(interface_info)

        _logger.info(self.network_connections)
        _logger.info(f"Network connections loaded! ({len(self.network_connections)})")