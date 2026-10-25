import os
import pynautobot
from dotenv import load_dotenv
import json

nb = pynautobot.api(
    "http://localhost:8080/",
    "c2fe8d5558da63757f71015448c7b55cf07302fc"
)

type = nb.dcim.device_types.all()
obj = nb.dcim.platforms.all()
d = nb.dcim.devices.all()
i = nb.dcim.interfaces.all()
ip = nb.ipam.ip_addresses.all()
r = nb.ipam.ip_address_to_interface.all()
p = nb.ipam.prefixes.all()
role = nb.extras.roles.all()
l = nb.dcim.locations.all()
devices_list = [dict(device) for device in ip]

print(json.dumps(devices_list, indent=4))