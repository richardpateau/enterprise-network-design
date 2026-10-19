import logging
from config import get_settings
from nautobot_client import NautobotClient
from device_connector import DeviceConnector
from auditor import ConfigDrift
from report_generator import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info(f"---- Starting Configuration Drift Detector ----")
    settings = get_settings()

    nautobot_client = NautobotClient(
        url=settings.get("nautobot_url"),
        token=settings.get("nautobot_token")
    )
    ssh_connection = DeviceConnector(
        username=settings.get("username"),
        password=settings.get("password"),
        secret=settings.get("secret")
    )
    report = ReportGenerator()
    target_devices = [("HQ-EDGE-1", "10.255.110.1"),
                      ("HQ-EDGE-2", "10.255.110.2"),
                      ("HQ-R1", "10.255.111.3")
                      ]
    audit_results = []
    for hostname, ip, in target_devices:
        logger.info(f"{'=' * 50}\nAuditing: {hostname} ({ip})")

        device, gold_configs = nautobot_client.get_nb_config(hostname)

        if not device:
            audit_results.append({
                "hostname": hostname,
                "status": "ERROR",
                "message": f"Device {hostname} not found in Nautobot",
                "drift_details": [],
                "total_changes": 0
            })
            continue
        ip_add = str(ip.split("/")[0])
        live_configs = ssh_connection.get_live_config(hostname, ip_add)
        if not live_configs:
            audit_results.append({
                "hostname": hostname,
                "status": "ERROR",
                "message": f"Couldn't Obtain Live Config",
                "drift_details": [],
                "total_changes": 0
            })
            continue

        drift_detector = ConfigDrift(hostname)
        result = drift_detector.compare_configs(gold_configs, live_configs)
        audit_results.append(result)

    logger.info("**** Generating HTML Report ****")
    report.html_report(audit_results)
    logger.info(f"==== Audit Successfully Completed ====")


if __name__ == "__main__":
    main()
