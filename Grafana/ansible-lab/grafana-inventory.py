import json
import os
from pathlib import Path

import pynautobot
from dotenv import load_dotenv

load_dotenv()

NAUTOBOT_URL = os.environ["NAUTOBOT_URL"]
NAUTOBOT_TOKEN = os.environ["NAUTOBOT_TOKEN"]

OUTPUT_FILE = Path("grafana_inventory.json")

nb = pynautobot.api(
    NAUTOBOT_URL,
    token=NAUTOBOT_TOKEN,
)

devices = nb.dcim.devices.all()

inventory = {}
skipped = []

for device in devices:
    location = getattr(device.location, "name", None)
    status = getattr(device.status, "name", None)

    if location != "New York" or status != "Active":
        continue

    primary_ip = None

    if device.primary_ip4:
        primary_ip = device.primary_ip4.address.split("/")[0]
    elif device.primary_ip6:
        primary_ip = device.primary_ip6.address.split("/")[0]

    if not primary_ip:
        skipped.append(device.name)
        continue

    inventory[device.name] = {
        "address": primary_ip,
        "location": location,
        "role": getattr(device.role, "name", None),
        "platform": getattr(device.platform, "name", None),
    }

output = {
    "devices": inventory,
    "skipped": skipped,
}

OUTPUT_FILE.write_text(
    json.dumps(output, indent=2),
    encoding="utf-8",
)

print(f"Monitoring targets: {len(inventory)}")
print(f"Skipped without primary IP: {len(skipped)}")

print("\nTargets:")
for name, data in inventory.items():
    print(f"  {name:15} {data['address']}")

if skipped:
    print("\nSkipped:")
    for name in skipped:
        print(f"  {name}")