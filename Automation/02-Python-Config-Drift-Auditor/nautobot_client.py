import pynautobot
import logging

logger = logging.getLogger(__name__)

class NautobotClient: 
	def __init__(self, url, token):
		self.nb = pynautobot.api(url=url, token=token)
		self.nb.http_session.verify = False 

	def get_nb_config(self, hostname):
		try:
			device = self.nb.dcim.devices.get(name=hostname)
			if not device:
				logger.error(f"Error: Device {hostname} not found in Nautobot")
				return None, None

			logger.info(f"--- Device {hostname} found in Nautobot ---")

			golden_config = device.comments if device.comments else ""

			if not golden_config:
				logger.warning(
						f"No Golden Config found | {hostname} | Nautobot"
					)
				return device, ""

			logger.info(f"Successfully Obtained Golden Config | {hostname}")
			return device, golden_config
		except Exception as e:
			logger.error(
					f"Try/Exception Error | {hostname} | {str(e)}"
				)
			return None, None