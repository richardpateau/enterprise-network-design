import requests
import logging

cert = '/home/rich/Documents/sysadmin-network.pem'
logger = logging.getLogger(__name__)

class ISE: 
	def __init__(self, url, username, password):
		self.base_url = f"{url}:9060/ers/config"
		self.auth = (username, password)

		self.headers = {
			'Content-Type': "application/json",
			'Accept': "application/json"
		}

	def check_ise_device(self, name):
		try:
			url = f"{self.base_url}/networkdevice/name/{name}"
			response = requests.get(url, auth=self.auth, headers=self.headers, verify=False)
			if response.status_code in [200, 201, 204]:
				logger.info(f"ISE: Device {name} is already configured.")
				return response.json()
			else:
				logger.error(f"Error: Device: {name} - Status Code: {response.status_code} - ({response.text})")
				return None
		except Exception as e:
			logger.error(
					f"Try/Exception Error: {name} - {str(e)}"
				)
			return None

	def configure_ise_device(self, name, ip_address, ise_radius_secret):
		try:
			if self.check_ise_device(name):
				return True


			payload ={
					"NetworkDevice": {
						"name": f"{name}",
						"description": "",
						"authenticationSettings": {
							"networkProtocol": "RADIUS",
							"radiusSharedSecret": f"{ise_radius_secret}",
							"enableKeyWrap": False,
							"dtlsRequired": False,
							"keyEncryptionKey": "",
							"messageAuthenticatorCodeKey": "",
							"keyInputFormat": "ASCII",
							"enableMultiSecret": "false"
						},
						"profileName": "Cisco",
						"coaPort": 1700,
						"NetworkDeviceIPList": [
							{
								"ipaddress": f"{ip_address}",
								"mask": 32
							}
						],
						"NetworkDeviceGroupList": [
							"Location#All Locations",
							"IPSEC#Is IPSEC Device#No",
							"Device Type#All Device Types"
						]
					}
				}

			url = f"{self.base_url}/networkdevice"
			response = requests.post(url, json=payload, headers=self.headers, auth=self.auth, verify=False)

			if response.status_code in [200, 201, 204]:
				logger.info(f"ISE: Device {name} - {ip_address} successfully configured.")
				return True
			else:
				logger.error(
						f"ISE: Failed to configure device {name} - {ip_address}"
					)

		except Exception as e:
			logger.error(
					f"Try/Exception Error: Device {name} - {ip_address} | {str(e)} "
				)

