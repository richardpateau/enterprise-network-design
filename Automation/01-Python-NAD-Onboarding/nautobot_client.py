import logging
import pynautobot

logger = logging.getLogger(__name__)


class NautobotClient:
    def __init__(self, url, token):
        self.nautobot = pynautobot.api(url, token)

        self.nautobot.http_session.verify = False

    def create_device(self, device_data):
        hostname = device_data['hostname']
        location_name = device_data['location_name']
        role_name = device_data['role_name']
        platform_name = device_data['platform_name']
        interfaces = device_data.get('interfaces', [])
        device_type_str = device_data.get("device_type")
        prefixes = device_data.get("prefixes", None)
        try:
            logger.info(f"--- Gathering Nautbot objects for {hostname} ---")

            #location
            location = self.nautobot.dcim.locations.get(name=location_name)
            if not location:
                logger.error(f"Location {location_name} not configured on Nautobot")
                logger.info(f"--- Configuring Location: {location_name} ---")
                location = self.nautobot.dcim.locations.create(name=location_name,
                                                         )
            #Role
            role=self.nautobot.extras.roles.get(name=role_name)
            if not role:
                logger.error(f"Role {role_name} not configured on Nautobot")
                logger.info(f"--- Configuring Role: {role_name} ---")
                role = self.nautobot.extras.roles.create(name=role_name,
                                                         content_types=["dcim.device"],
                                                         )
            #Platforms
            platform = self.nautobot.dcim.platforms.get(name=platform_name)
            if not platform:
                logger.error(f"Platform {platform_name} not configured on Nautobot")
                logger.info(f"--- Configuring Platform: {platform_name} ---")
                platform = self.nautobot.dcim.platform_name.create(name=platform_name)

            device_type = self.nautobot.dcim.device_types.get(model=device_type_str)
            if not device_type:
                logger.error(f"Device Type {device_type} not configured on Nautobot")
                logger.info(f"--- Configuring Device Type: {platform_name} ---")
                device_type  = self.nautobot.dcim.device_types.create(model=device_type_str,
                                                                      manufacturer="Cisco"
                                                                      )

            device = self.nautobot.dcim.devices.get(name=hostname)

            if not device:
                logger.info(f"---- Creating Nautbot Entry for {hostname} ----")
                device = self.nautobot.dcim.devices.create(
                        name=hostname,
                        device_type=self.nautobot.dcim.device_types.get(model=device_type_str).id,
                        role=role.id,
                        location=self.nautobot.dcim.locations.get(name=location).id,
                        platform=self.nautobot.dcim.platforms.get(name=platform_name).id,
                        status="Active"
                    )
                logger.info(f"**** Nautobot Device Configuraiton Successful: {hostname}")
            else:
                logger.info(f"Device: {hostname} already configured.")
            device_id = device.id
            if prefixes:
                prefixes_list = list(self.nautobot.ipam.prefixes.all())
                prefix_list = [p.prefix for p in prefixes_list]
                logger.debug(f"{prefix_list}")
                for p in prefixes:
                    if p in prefix_list:
                        continue
                    logger.info(f"--- Configuring Device Prefixes for {hostname} ---")
                    self.nautobot.ipam.prefixes.create(
                            prefix=str(p),
                            status="Active"
                        )
                    logger.info(f"Prefix {p} Successfully Configured Device {hostname}")

            for interface in interfaces:
                interface_name = interface.get("name", None)
                description = interface.get("description", "")
                is_mgmt = interface.get("is_mgmt", None)
                mode = interface.get("mode", None)
                type = interface.get("type", "100BASE-TX(10/100ME)")
                ip_address = interface.get("ip_address")
                interface_kwargs = {
                    "device":device_id,
                    "name": interface_name,
                    "description": description,
                    "type": type,
                    "status": "Active"
                }

                if mode:
                    interface_kwargs["mode"] = mode

                interface_obj = self.nautobot.dcim.interfaces.get(name=interface_name, device=hostname)
                if not interface_obj:
                    logger.info(f"--- Creating Interface {interface_name} Nautbot Config: {hostname} ----")
                    self.nautobot.dcim.interfaces.create(
                            **interface_kwargs
                        )
                    logger.info(f"Successfully Configured Nautobot Interface {interface_name} for {hostname}")
                else:
                    logger.info(f"Interface {interface_name} for Nautobot already configured: {hostname}")
                if ip_address:
                    target_ip = self.nautobot.ipam.ip_addresses.get(address=ip_address)
                    if not target_ip:
                        logger.info(f"--- Creating IP address Nautobot Config: {hostname} - {ip_address} ----")
                        target_ip = self.nautobot.ipam.ip_addresses.create(
                            address=ip_address,
                            status="Active",
                            namespace="Global"
                        )
                        logger.info(f"IP address on Nautobot Successfully Configured: {hostname} - {ip_address} ----")
                    target_interface = self.nautobot.dcim.interfaces.get(
                        name=interface_name,
                        device=hostname)
                    if not target_interface:
                        logger.error(
                            f"Error: Interface {interface_name} not found during IP configuration"
                        )
                        continue
                    assignment = self.nautobot.ipam.ip_address_to_interface.get(
                        ip_address=target_ip.id,
                        interface=target_interface.id
                    )
                    logger.info(f"IP-Interface Assignment Verified: {target_ip} - {target_interface}")
                    if not assignment:
                        logger.info(f"---- Assigning {ip_address} to {interface_name} ----")
                        self.nautobot.ipam.ip_address_to_interface.create(
                            interface=target_interface.id,
                            ip_address=target_ip.id
                        )
                        logger.info(f"Successfully Assigned Nautobot IP to Interface Binding for {hostname} - {ip_address} - {interface_name}")
            return device

        except Exception as e:
            logger.error(
                f"Try/Exception Error: {hostname} | "
                f"{str(e)}"
            )
            return False
    def mgmt_ip(self, device_data):
        interfaces = device_data.get('interfaces', [])
        hostname= device_data.get("hostname")
        try:
            device = self.nautobot.dcim.devices.get(name=hostname)
            if not device:
                logger.error(f"Nautobot device not found: {hostname}")
                return None
            if device.primary_ip4:
                logger.info(f"Primary IPv4 Already Configured - {device.primary_ip4.address}")
                return device
            for interface in interfaces:
                interface_name = interface.get("name")
                ip_address = interface.get("ip_address")
                if interface.get("is_mgmt"):
                    logger.info(f"Configuring Nautobot Primary IPv4 for {ip_address} - {hostname}")
                    target_ip = self.nautobot.ipam.ip_addresses.get(
                        address=ip_address
                    )
                    if not target_ip:
                        logger.error(f"Error: Interface {interface_name} has no IP")
                        return None
                    device.update({
                        "primary_ip4": target_ip.id
                    })
                    logger.info(f"Successfully Configured Nautobot Primary IPv4 for {hostname} - {ip_address}")
                    device = self.nautobot.dcim.devices.get(name=hostname)


            logger.info(f"**** Successfully created Nautobot entry for: {hostname} ****")
            return device
        except Exception as e:
            logger.error(f"Try/Exception Error: {str(e)}")
