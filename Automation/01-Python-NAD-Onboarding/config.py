import os 
from dotenv import load_dotenv

def credentials():
	load_dotenv()

	return {
		"nautobot_url": os.getenv("NAUTOBOT_URL"),
		"nautobot_token": os.getenv("NAUTOBOT_TOKEN"),
		"ise_url": os.getenv("ISE_URL"),
		"ise_username": os.getenv("ISE_USERNAME"),
		"ise_password": os.getenv("ISE_PASSWORD"),
		"ise_radius_secret": os.getenv("ISE_RADIUS_SECRET")
	}

