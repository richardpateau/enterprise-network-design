import os
from datetime import datetime
from pathlib import Path
import pynautobot
from dotenv import load_dotenv
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import  NetmikoTimeoutException
ssh_config = os.path.expanduser("~/.ssh/config")

load_dotenv()
url = os.getenv("NAUTOBOT_URL")
token = os.getenv("NAUTOBOT_TOKEN")
username = os.getenv("SSH_USERNAME")
password = os.getenv("SSH_PASSWORD")
secret = os.getenv("SECRET")
asa_password = os.getenv("ASA_PASSWORD")
asa_enable = os.getenv("ASA_ENABLE")
required = {
        "NAUTOBOT_URL": url,
        "NAUTOBOT_TOKEN": token,
        "SSH_USERNAME": username,
        "SSH_PASSWORD": password,
        "ASA_PASSWORD": asa_password,
        "SECRET": secret
        }

missing = [name for name, value in required.items() if not value]

if missing:
    raise SystemExit(
        f"Missing environment variables: {', '.join(missing)}"
    )

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

backup_root = Path("configs-backups") / timestamp
backup_root.mkdir(parents=True, exist_ok=True)

print(f"Connecting to Nautobot: {url}")

nautobot = pynautobot.api(url, token)

devices = nautobot.dcim.devices.all()
print("Retreiving devices from Nautobot")

successful = []
failed = []

for device in devices:
    name = device.name

    if not name:
        print("Device in SOT is unnamed, skipping...")
        continue
    if "SW" in name:
        continue
    if "INTERNAL" in name:
        continue
    primary_ip = None

    if device.primary_ip4:
        primary_ip = str(device.primary_ip4.address).split("/")[0]

    if not primary_ip:
        print(f"Error: No IP address, skipping device {name}")
        failed.append((name, "No Primary IP"))
        continue

    if "FW" not in name:
        connection = {
                "device_type": "cisco_ios",
                "host": primary_ip,
                "username": username,
                "password": password,
                "secret": secret,
                "timeout": 360,
        }
    else:
        connection = {
            "device_type": "cisco_asa",
            "host": primary_ip,
            "username": username,
            "password": asa_password,
            "secret": asa_enable,
            "timeout": 360,
            "global_delay_factor": 2,
            "fast_cli": False,
        }

    try:
        with ConnectHandler(**connection) as conn:

            conn.enable()
            print(f"--- Connected to {name} - {primary_ip} ---")

            show_run = conn.send_command("show running-config", read_timeout=360)

            filename = backup_root / f"{name}.cfg"

            filename.write_text(show_run, encoding="utf-8")
            successful.append(name)
            print(f"Saved: {filename}")

    except NetmikoTimeoutException:
        print(f"Try / Exception Error - Timeout: {name}")
        failed.append(
            (name, "Connection Timeout")
        )
    except NetmikoAuthenticationException:
        print(f"Try / Exception Error - Authentication: {name}")
        failed.append(
            (name, "Authentication Error")
        )
    except Exception as error:
        print(f"Try/Exception Error {name} : {error}")
        failed.append((name, str(error)))


print(f"Backup directory: {backup_root}")
print(f"Successful: {len(successful)}")
print(f"Failed:     {len(failed)}")

if successful:
    print("Successful backups:")
    for name in successful:
        print(f"[Pass] {name}")

if failed:
    print("Failed Backups")
    for name in failed:
        print(f"[Failed] {name}")

print("Backup Complete")