from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
import logging

logger = logging.getLogger(__name__)

class DeviceConnector:
	def __init__(self, username, password, secret):
		self.username = username
		self.password = password
		self.secret = secret 

	def get_live_config(self, hostname, ip_address): 
		device_settings = {
			"device_type": "cisco_ios",
			"host": ip_address,
			"username": self.username,
			"password": self.password,
			"secret": self.secret,
		}

		try: 
			logger.info(
					f"---- Connecting to {hostname} - {ip_address} via Netmiko ----"
				)

			conn = ConnectHandler(**device_settings, timeout=30)

			conn.enable()

			logger.info("---- SSH session started ----")
			live_config = conn.send_command("show running-config", read_timeout=150)

			conn.disconnect()

			logger.info(f"{hostname} - Successfully Obtained Running-Config")
			return live_config 

		except NetmikoAuthenticationException: 
			logger.error(
					f"Authentication Failure - {hostname}"
				)
			return None 
		except NetmikoTimeoutException: 
			logger.error(
					f"Timeout Error - {hostname}"
				)
			return None
		except Exception as e: 
			logger.error(
					f"Try/Exception Error: {hostname} - {str(e)}"
				)
			return None 
