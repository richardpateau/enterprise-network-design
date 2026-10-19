# config.py
import os
from dotenv import load_dotenv

def get_settings():
    load_dotenv()
    return {
        "nautobot_url": os.getenv("NAUTOBOT_URL"),
        "nautobot_token": os.getenv("NAUTOBOT_TOKEN"),
        "username": os.getenv("DEVICE_USERNAME"),
        "password": os.getenv("DEVICE_PASSWORD"),
        "secret": os.getenv("DEVICE_SECRET"),
        "jira_url": os.getenv("JIRA_URL"),
        "jira_email": os.getenv("JIRA_EMAIL"),
        "jira_token": os.getenv("JIRA_API_TOKEN"),
        "jira_project_key": os.getenv("JIRA_PROJECT_KEY")
    }
