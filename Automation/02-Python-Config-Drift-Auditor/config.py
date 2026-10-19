import os
from dotenv import load_dotenv

def get_settings():
    load_dotenv()
    return {
        "nautobot_url": os.getenv("NAUTOBOT_URL"),
        "nautobot_token": os.getenv("NAUTOBOT_TOKEN"),
        "username": os.getenv("DEVICE_USERNAME"),
        "password": os.getenv("DEVICE_PASSWORD"),
        "secret": os.getenv("DEVICE_SECRET")
    }
