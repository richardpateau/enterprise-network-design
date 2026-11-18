import json
import sys 
import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FORTINET_IP = "192.168.255.10"
FORTINET_API = "k9ywsGfqdsdk7ry155wf0wmx4h3gk9"
FORTINET_BASE_URL = f"https://{FORTINET_IP}/api/v2"

headers = {
	"Authorization": f"Bearer {FORTINET_API}",
    "Content-Type": "application/json",
    "Accept": "application/json"
	}

def query_sdwan_health(): 
	print (
			f"------ Step 1: Querying Live SD-WAN Memnbers Health Metrics"
		)
	url = f"{FORTINET_BASE_URL}/monitor/virtual-wan/member-health"

	try: 
		response = requests.get(
				url, headers=headers, verify=False, timeout=120
			)

		if response.status.code in [200,201,204]:
			print(
					f"		[SUCCESS] HTTP 200 OK - Fortinet API"
				)
			data = response.json()
			print(data)
			results = data.get("results", [])
	except Exception as e:
		print(f"Error: {str(e)}")

