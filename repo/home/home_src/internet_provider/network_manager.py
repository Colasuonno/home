import logging
import psutil
import socket

_logger = logging.getLogger(__name__)

class HomeNetworkManager:

    def __init__(self):

        # Visualize current network manager and store it
        interfaces = psutil.net_if_addrs()
        connections = psutil.net_if_stats()

        for interface, addresses in interfaces.items():
            _logger.info(f"Interface: {interface}")

            if interface in connections:
                _logger.info(f"  Status: {'Up' if connections[interface].isup else 'Down'}")
                _logger.info(f"  Speed: {connections[interface].speed} Mbps" if connections[
                    interface].speed else "  Speed: Unknown")

            for addr in addresses:
                if addr.family == socket.AF_INET:
                    _logger.info(f"  IPv4 Address: {addr.address}")
                    _logger.info(f"  Netmask: {addr.netmask}")
                elif addr.family == socket.AF_INET6:
                    _logger.info(f"  IPv6 Address: {addr.address}")
                elif addr.family == psutil.AF_LINK:
                    _logger.info(f"  MAC Address: {addr.address}")

            _logger.info("-" * 40)