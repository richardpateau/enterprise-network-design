import csv
import logging
from config import credentials
from nautobot_client import NautobotClient
from ise_client import ISE
import yaml
import urllib3

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    logger.info("--- Starting Automated ISE Onboarding ---")

    settings = credentials()

    nautobot_client = NautobotClient(
        url=settings.get("nautobot_url"),
        token=settings.get("nautobot_token")
    )

    ise_client = ISE(
        url=settings.get("ise_url"),
        username=settings.get("ise_username"),
        password=settings.get("ise_password")
    )

    ise_radius_secret = settings.get("ise_radius_secret")
    yaml_file = "inventory.yml"
    csv_file = "new_devices.csv"
    logger.info("--- Reading devices from YAML file ---")

    try:
        with open(yaml_file, "r") as file:
            data = yaml.safe_load(file) or {}
            devices = data.get("devices", [])

            for device in devices:
                hostname = device.get("hostname")
                logger.info(f"{'='*50}\nProcessing Device: {hostname}")

                create_device = nautobot_client.create_device(device)
                nb_device = nautobot_client.mgmt_ip(device)
                if not nb_device:
                    logger.info(
                            f"Skipping ISE Configuration for {hostname} | "
                            f"Nautobot Failure"
                        )
                    continue
                primary_ip = nb_device.primary_ip4
                official_ip = primary_ip.address.split("/")[0]
                print(f"{official_ip}")
                if not primary_ip:
                    logger.error(f"Error: Host {hostname} Missing Primary IPv4")
                    continue
                if official_ip:
                    ise_success = ise_client.configure_ise_device(
                            name=hostname,
                            ip_address=official_ip,
                            ise_radius_secret=ise_radius_secret

                        )
                    if not ise_success:
                        logger.info(f"ISE: Failure at {hostname}")
                else: 
                    logger.info(f"Error: ISE skipping {hostname} due to missing management IP (nautobot)")
        logger.info(f"{'=' * 50}")
        logger.info("Workflow completed successfully!")

    except FileNotFoundError:
        logger.error(f"Error: Could not find {csv_file}.")
    except Exception as e:
        logger.error(f"Try/Exception Error: {str(e)}")

if __name__ == "__main__":
    main()
