import logging
from config import get_settings
from jira_client import JiraClient
from switch_provisioner import SwitchProvisioner

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
	logger.info(
			f"---- Starting Jira to Configuration Automation ----"
		)
	settings = get_settings()
	jira_client = JiraClient(
			settings["jira_url"],
			settings.get("jira_email"),
			settings.get("jira_token")
		)
	switch_client = SwitchProvisioner(settings)

	tickets = jira_client.get_ticket(settings.get("jira_key"))

	if not tickets: 
		logger.error(
				f"ERROR: There are no open Tickets in Jira"
			)
		return 

	for t in tickets: 
		logger.info(f"{'='*50}")

		jira_client.progress_ticket(t.get("self_url"))

		switch_client.configure_port(t)

	logger.info(
			f"##### Jira to Configurtion Workflow Successfully Completed #####"
		)

if __name__=="__main__":
	main()