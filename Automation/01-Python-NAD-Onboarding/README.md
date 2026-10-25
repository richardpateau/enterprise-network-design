# Automated Day-1 Zero-Touch Provisioning (Nautobot ➔ Cisco ISE)

##  Executive Summary
This project is a production-grade Python automation framework designed to eliminate manual data entry during network device deployment. By ingesting a structured YAML/CSV inventory, the script automatically provisions device records in **Nautobot** (establishing the Single Source of Truth) and simultaneously registers the devices as Network Access Devices (NADs) in **Cisco ISE** with secure RADIUS shared secrets. 

This tool reduces device onboarding time from hours to seconds, eliminates human error, and ensures 100% data integrity across the network management stack.

**Automated Cisco ISE and Nautobot: 16 devices in 4:17!**
**Please enlarge for clearer video**

https://github.com/user-attachments/assets/b05e784b-5f10-4eed-bbde-ac6dc558a46c

![Automation](screenshots/time.png)

---

## Architecture & Design Patterns

### 1. Modular Object-Oriented Design
The codebase is strictly separated into logical modules to ensure maintainability and reusability:
*   `main.py`: The orchestrator that parses data and directs workflow.
*   `nautobot_client.py`: Dedicated class for Nautobot API interactions and IPAM logic.
*   `ise_client.py`: Dedicated class for Cisco ISE ERS API interactions.
*   `config.py`: Securely loads credentials from environment variables.

### 2. Data-Driven Automation
Instead of hardcoding device details, the script ingests external data (`inventory.yaml`). This allows the exact same script to onboard 1 device or 1,000 devices without modifying a single line of Python code.

### 3. Strict Data Integrity (The Nautobot Relational Model)
Nautobot requires strict relational binding. The script respects this by:
1. Creating the physical/virtual Interface object.
2. Creating the IP Address object in IPAM.
3. Binding the IP Address to the Interface (`assigned_object_id`).
4. *Only then* setting the device's `primary_ip4` field. 

### 4. Idempotency
The script is entirely idempotent. It checks for the existence of Locations, Roles, Interfaces, and IPs before attempting creation. It can be run repeatedly against the same inventory without generating duplicate records or API errors.

**No configuration needed**

![Automation](screenshots/already-configured-log.png)

**Needs a configuration**

![Automation](screenshots/terminal-output.png)
---

## Key Technical Features

*   **Nautobot v3 Compatibility:** Utilizes the modern `Locations` hierarchy instead of legacy `Sites`.
*   **Dynamic Interface Typing:** Automatically parses Cisco interface names (e.g., `TenGigabitEthernet`, `Loopback`) to assign the correct Nautobot slug (`10gbase-x-sfpp`, `virtual`), while allowing manual YAML overrides.
*   **Layer 2 & Layer 3 Agnostic:** Seamlessly handles routed interfaces (assigning IPs) and switched interfaces (applying Access/Trunk modes) in the same execution.
*   **Cisco ISE ERS API Integration:** Automatically provisions NADs with correct Network Device Groups (NDGs) and secure RADIUS shared secrets.
*   **Security First:** All sensitive credentials (API tokens, RADIUS secrets) are strictly managed via `.env` files and excluded from version control.

---

## Workflow Diagram

![Automation](screenshots/nad-automation-visio.png)

---

## Prerequisites & Setup

1. **Python Environment:** Python 3.8+
2. **Dependencies:** `pip install -r requirements.txt`
3. **Environment Variables:** Create a `.env` file in the root directory:
   ```env
   NAUTOBOT_URL=http://localhost:8080
   NAUTOBOT_TOKEN=your_nautobot_token
   ISE_URL=https://your-ise-pan-ip
   ISE_ERS_USER=ers_admin
   ISE_ERS_PASS=your_ise_password
   ISE_RADIUS_SECRET=your_radius_secret
   ```
4. **Inventory:** Populate `inventory.yaml` with target hardware.

---

## Portfolio Evidence & Execution

Below is visual proof of the automation workflow in action.

### 1. Initial State (Before Automation)

**Nautobot Devices**

![Automation](screenshots/before-nauto-bot-devices.png)

**Nautobot IP addresses**

![Automation](screenshots/before-ipam.png)

**Nautobot Prefixes**

![Automation](screenshots/before-prefixes.png)

**ISE: Network Devices**

![Automation](screenshots/before-ise.png)

### 2. Script Execution

**Terminal Output**

![Automation](screenshots/already-configured-log.png)


![Automation](screenshots/terminal-output.png)

### 3. Nautobot Post-Provisioning

**Devices created with correct Roles and Locations**

![Automation](screenshots/devices-post-script.png)

![Automation](screenshots/device-interfaces.png)

**Interfaces correctly typed (1000BASE-T vs Virtual) and attached to devices.**

![Automation](screenshots/interface_types.png)

**IPAM populated with prefixes and IPs correctly bound to interfaces.**

![Automation](screenshots/ipam-addresses-after.png)

![Automation](screenshots/prefixes-after.png)

![Automation](screenshots/interface-to-ip.png)

### 4. Cisco ISE Post-Provisioning
*NADs automatically created with RADIUS autoconfig settings.*

**Full List**

![Automation](screenshots/ise-after.png)

![Automation](screenshots/ise-after-2.png)

**RADIUS Authentication**

![Automation](screenshots/ise-radius.png)

---

---

### What's Next?

With Day-1 Zero-Touch Provisioning fully automated and validated, the next step is to ensure ongoing configuration compliance and detect unauthorized changes.

Continue to the next module to explore Configuration Drift Auditing:
- **[02 — Day 2 Configuration Drift Auditor & Alerting](../02-Python-Config-Drift-Auditor/)** – Netmiko-based config comparison and HTML compliance reports.
