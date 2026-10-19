
from netmiko import ConnectHandler
import logging
import getpass
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    host = "10.255.110.1"

    username = input("Telnet username: ")
    password = getpass.getpass("Telnet password: ")
    secret = getpass.getpass("Enable secret: ")

    device = {
        "device_type": "cisco_ios_telnet",
        "host": host,
        "username": username,
        "password": password,
        "secret": secret,
        "port": 23,
        "conn_timeout": 15,
        "auth_timeout": 15,
        "banner_timeout": 15,
        "fast_cli": False,
    }

    connection = None

    try:
        print(f"\nConnecting to {host} over Telnet...")

        connection = ConnectHandler(**device)
        print("[SUCCESS] Telnet session established.")

        print("\nEntering enable mode...")
        connection.enable()
        print("[SUCCESS] Enable mode entered.")

        print("\nRetrieving running configuration...")
        output = connection.send_command(
            "show running-config",
            read_timeout=60,
        )

        if output and output.strip():
            print("\n" + "=" * 70)
            print("RUNNING CONFIGURATION")
            print("=" * 70)
            print(output)
            print("=" * 70)
            print(f"\nCharacters received: {len(output)}")
        else:
            print("[ERROR] Running configuration was empty.")

    except Exception:
        logging.exception("Telnet test failed.")
        sys.exit(1)

    finally:
        if connection is not None:
            connection.disconnect()
            print("\nTelnet session closed.")

if __name__ == "__main__":
    main()
