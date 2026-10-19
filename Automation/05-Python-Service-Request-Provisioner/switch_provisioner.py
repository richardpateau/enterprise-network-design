import re 
import logging

import requests
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
from jinja2 import Environment, FileSystemLoader
from jira_client import JiraClient
import json
logger = logging.getLogger(__name__)

class SwitchProvisioner:
	def __init__(self, settings): 
		self.settings = settings
		
		self.jira_client = JiraClient(
				settings.get("jira_url"),
				settings.get("jira_email"),
				settings.get("jira_token")
			)

		self.jinja_env = Environment(loader=FileSystemLoader('templates'))

	def parse_jira_ticket(self, description):
		data = {}

		parsed_data = {
			"target_device": r"Target Device:\s*(.+)",
			"target_interface": r"Target Interface:\s*(.+)",
			"vlan_id": r"VLAN ID:\s*(.+)",
			"vlan_name": r"VLAN Name:\s*(.+)",
			"port_description": r"Port Description:\s*(.+)",
			"voice_vlan": r"Voice VLAN:\s*(.+)"
		}
		if isinstance(description, dict):
			description = "\n".join(
				item.get("text", "")
				for block in description.get("content", [])
				for item in block.get("content", [])
				if item.get("type") == "text"
			)
		for k,v in parsed_data.items():
			match = re.search(v, description, re.IGNORECASE)
			if match:
				data[k] = match.group(1).strip()

		return data

	def configure_port(self, ticket):
		ticket_key = ticket.get('key')
		description = ticket.get('description')
		logger.info(
				f"---- Processing Ticket: {ticket_key} ----"
			)

		config_data = self.parse_jira_ticket(description)
		if not config_data:
			failure_message = "Failed to Parse Ticket | Missing Description"
			logger.error(failure_message)
			self.update_jira_ticket({
					ticket.get("self_url"),
					"Failed",
					failure_message
			})
			return

		logger.info(f"Parsed Data: {config_data}")

		template = self.jinja_env.get_template("port_provision.j2")
		config_data["ticket_id"] = ticket_key
		template_render = template.render(**config_data)

		device_netmiko = {
			"device_type": "cisco_ios",
			"host": config_data.get("target_device"),
			"username": self.settings.get("username"),
			"password": self.settings.get("password"),
			"secret": self.settings.get("secret"),
			"timeout": 100
		}
		try:
			logger.info(
					f"---- Starting Configuration Change {config_data.get("target_device").split('"')[0]} ----"
				)
			conn = ConnectHandler(**device_netmiko)

			conn.enable()

			conn.send_config_set(template_render.splitlines(), read_timeout=120)

			conn.save_config()
			conn.disconnect()

			logger.info(
					f"**** Device {config_data.get('target_device')} Successfully Configured ****"
				)
			success_message = (
					f"SUCCESS - {config_data.get('target_device')}"
					f"Interface: {config_data.get('target_interface')}"
				)
			self.update_jira_ticket(
						ticket.get("self_url"),
						"Completed",
						success_message
			)
		except NetmikoAuthenticationException:
			error_message = "Authentication Failed. Check Credentials"
			logger.error(error_message)
			self.update_jira_ticket(
						ticket.get("self_url"),
						"Failed",
						error_message
			)
		except NetmikoTimeoutException:
			error_message = "Timeout Failure"
			logger.error(error_message)
			self.update_jira_ticket(
						ticket.get("self_url"),
						"Failed",
						error_message
			)
		except Exception as e:
			error_message = f"{str(e)}"
			logger.error(error_message)
			self.update_jira_ticket(ticket.get("self_url"),"Failed",error_message)
	def update_jira_ticket(self, self_url, status, message):
		try:

			transition_endpoint = f"{self_url}/transitions"
			payload = {"transition": {"id": "111"}}

			update_response = requests.post(
					transition_endpoint, auth=self.jira_client.auth,
					headers=self.jira_client.headers, json=payload
				)
			if update_response.status_code in [200,201,204]:
				logger.info(
						f"Ticket {status} - Moved To Completed | {self_url}"
					)
			else:
				logger.warning(
						f"ERROR - {self_url}: Failed to Move Jira Ticket to Completed"
						f"{update_response.text}"
					)
		except Exception as e:
			logger.error(
					f"Try/Exception Error: {self_url} | {str(e)}"
				)
