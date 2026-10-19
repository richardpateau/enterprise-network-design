import requests
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger(__name__)

class JiraClient:
	def __init__(self, url, email, token):
		self.url = url.rstrip('/')
		self.auth = HTTPBasicAuth(email, token)
		self.headers = {
			"Accept": "application/json", 
			"Content-Type": "application/json"
		}

	def get_ticket(self, project_key):
		jira_query = f"project = SUP AND status = 'Open' AND summary ~ 'Port Provisioning' ORDER BY created ASC"

		endpoint_url = f"{self.url}/rest/api/3/search/jql"

		parameters = {
			"jql": jira_query,
			"maxResults": 10,
			"fields": "summary,description,status"
		}

		try: 
			logger.info(
					f"---- Gathering Jira Tickets ----"
				)
			response = requests.get(endpoint_url, auth=self.auth, 
									headers=self.headers, params=parameters)

			if response.status_code in [200,201,204]: 
				data = response.json()
				issues =  data.get('issues', [])

				if issues: 
					logger.info(
							f"**** Found {len(issues)} unresolved tickets ****"
						)
				tickets = []

				for i in issues: 
					tickets.append({
							"key": i.get("key"),
							"summary": i.get("fields").get("summary"),
							"description": i.get("fields").get("description"),
							"self_url": i.get("self")
						})
			else: 
				logger.error(
						f"ERROR: Failed to get tickets | {response.status_code} | {response.text}"
					)
			return tickets
		except Exception as e: 
			logger.error(
					f"Try/Exception Error: Jira Query | {str(e)}"
				)
	def progress_ticket(self, self_url):
		try: 
			progress_endpoint = f"{self_url}/transitions"
			progress_repsonse = requests.get(progress_endpoint, auth=self.auth, headers=self.headers)

			if progress_repsonse in [200,201,204]: 
				logger.error(
						f"Failed to find Jira Ticket | {self.url}"
					)
				return False 

			transitions = progress_repsonse.json().get('transitions', [])
			logger.info(f"---- Processing Jira Ticket ----")
			in_progress_id = None 
			for t in transitions: 
				name = t.get("name").lower()
				to_name = t.get("to").get("name").lower()

				if "investigate" in name and "progress" in to_name: 
					in_progress_id = t.get("id")
					logger.info(f"Jira Transition Found | {name} | ID: {in_progress_id}")
					break 

			if not in_progress_id: 	
				logger.warning(
						f"Could not Find 'In Progress' transitions"
					)
				return False 
			payload = {"transition": {"id": in_progress_id}}
			update_response = requests.post(progress_endpoint, auth=self.auth, headers=self.headers, json=payload)
			if update_response.status_code in [200,201,204]: 
				logger.info(
						f"**** Jira Ticket Successfully moved to 'In Progres' | {self.url}"
					)
			else: 
				logger.error(
						f"**** Failed to Transition Jira Ticket | {self.url} ****"
					)
		except Exception as e: 
			logger.error(
					f"Try/Exception Error: Jira Ticket | {self.url} | {str(e)}"
				)