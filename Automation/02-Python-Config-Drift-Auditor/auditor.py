import difflib
import logging 
import re 

logger = logging.getLogger(__name__)

class ConfigDrift: 
	def __init__(self, hostname): 
		self.hostname = hostname

	def strip_config(self, config_text):
		if not config_text:
			return ""

		lines = str(config_text).splitlines()
		adjusted_lines = []

		ignore = [
		r"^!.*Last configuration change at.*",
		r"^!.*Building configuration...*",
		r"^!.* *",
		r"^!.*NVRAM config last updated at.*",
		r"^version.*",
		r"^ntp clock-period.*",
		r"^crypto pki certificate chain.*",
		r"^!.*"
			]

		for line in lines:
			new_line = line.strip()
			if not new_line:
				continue
			#Regex or Conditionals can be used to clean lines
			if "Building configuration" in line:
				continue

			if any(re.match(i, line.strip(), re.IGNORECASE) for i in ignore):
				continue

			adjusted_lines.append(line)

		return "\n".join(adjusted_lines)

	def compare_configs(self, golden_config, live_config):
		logger.info(
				f"---- Starting Configuration Diff Audit ----"
			)

		golden_configs = self.strip_config(golden_config)
		if not golden_configs:
			logger.warning(
					f"Error: Golden Config is Empty | {self.hostname}"
				)
			return {
					"status": "ERROR",
					"hostname": self.hostname,
					"drift_details": [],
					"total_changes": 0,
					"message": "Empty Golden Configuration"
				}
		live_configs = self.strip_config(live_config)
		if not live_configs:
			logger.warning(
				f"Error: Live Config is Empty | {self.hostname}"
			)
			return {
				"status": "ERROR",
				"hostname": self.hostname,
				"drift_details": [],
				"total_changes": 0,
				"message": "Empty Live Configuration"
			}

		difference = list(difflib.ndiff(golden_configs.splitlines(), live_configs.splitlines()))
		drift_details = []

		for line in difference:
			if line.startswith("- "):
				drift_details.append({
						"type": "Removed",
						"line": line[2:].strip(),
						"description": "Configuration taken out of Golden Config (Missing)"
					})
			elif line.startswith("+ "):
				drift_details.append({
							"type": "Added",
							"line": line[2:].strip(),
							"description": "Extra Configuration Added to Golden Config"
					})
		drift_detected = bool(drift_details)
		if drift_detected:
			status = "FAILURE"
			logger.warning(f"**** Drift Detected | {self.hostname} | Total Changes: {len(drift_details)} ****")
		else:
			status = "SUCCESS"
			logger.info(f"**** Device Compliant | {self.hostname}")

		return {
			"hostname": self.hostname,
			"drift_detected": drift_detected,
			"drift_details": drift_details,
			"status": status,
			"total_changes": len(drift_details),
			"message": ""
		}