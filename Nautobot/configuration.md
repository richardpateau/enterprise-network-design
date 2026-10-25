# Nautobot Configuration & Automation Integration

## Overview

This document details the Nautobot Source of Truth (SOT) implementation for the Meridian Financial Services network, including data model configuration, API integration via `pynautobot`, and automation workflows.

![nautobot](screenshots/nautobot-json-print-script.png)

---

## 1. Data Model Configuration

### 1.1 Location GUI and API Object 

The enterprise network is structured using Nautobot's location hierarchy, organizing devices by geographic site and functional role.

**Evidence:**
- Location objects configured for all five sites (New York HQ, Chicago, Dallas, Miami, Ashburn DR)
- Devices assigned to appropriate sites with role classifications

**GUI**

![nautobot](screenshots/location-gui.png)

**API Python Object**

![nautobot](screenshots/location-object-json.png)

### 1.2 Device Inventory GUI and API Object

Network devices are registered in Nautobot with complete metadata including:
- **Device Name:** Hostname matching the running configuration
- **Device Role:** wan-edge, core-router, access-switch, firewall
- **Platform:** Cisco IOS, IOS-XE, ASA
- **Site:** Geographic location assignment
- **Status:** Active/Inactive state tracking

**API Response Example (MIA-R2):**
The device object JSON demonstrates the rich metadata available via the API, including nested references to device_type, status, role, and tenant relationships.

**GUI**

![nautobot](screenshots/nautobot-device-list-1.png)

![nautobot](screenshots/mia-r2-gui.png)

![nautobot](screenshots/device-role-overview.png)

**API Python Object**

![nautobot](screenshots/device-object-json-mia-r2.png)

### 1.3 Interface Configuration GUI and API Object

Interfaces are modeled with detailed attributes to support automation:
- **Interface Name:** Matches exact device configuration (e.g., `FastEthernet0/0`)
- **Description:** Documents the connected endpoint (e.g., `WAN-TO-EDGE-1`)
- **Type:** Interface speed/capability (100BASE-TX, 1000BASE-T, etc.)
- **Enabled State:** Tracks administrative status
- **Device Relationship:** Links interface to parent device

**GUI**

![nautobot](screenshots/interface-gui-ash-r1.png)

**API Python Object**

![nautobot](screenshots/interface-object-json.png)

---

## 2. IP Address Management (IPAM) GUI and API Object

### 2.1 Prefix Hierarchy

The IPAM structure mirrors the enterprise addressing plan with proper hierarchy:

| Prefix Block | Purpose | Sites |
| :--- | :--- | :--- |
| `10.10.0.0/16` | New York HQ | HQ VLANs 10-70 |
| `10.20.0.0/16` | Chicago Branch | VLANs 10-70 |
| `10.30.0.0/16` | Dallas Branch | VLANs 10-70 |
| `10.40.0.0/16` | Miami Branch | VLANs 10-70 |
| `10.50.0.0/16` | Ashburn DR | VLANs 110-150 |
| `172.16.0.0/16` | WAN Links | Point-to-point /30s |
| `10.255.0.0/16` | Loopbacks | Router/switch loopbacks |

**GUI**

![nautobot](screenshots/prefixes.png)

**API Python Object**

![nautobot](screenshots/prefix-object.png)

### 2.2 IP Address Assignments

Individual IP addresses are tracked with interface-level granularity:

**WAN Addressing (Point-to-Point /30s):**
```
172.16.0.1/30   → FastEthernet0/0
172.16.0.5/30   → FastEthernet1/0
172.16.0.9/30   → FastEthernet2/0
172.16.1.1/30   → FastEthernet0/0
```

**LAN Addressing (VLAN SVIs):**
```
10.20.10.2/24   → FastEthernet0/0.10 (VLAN 10)
10.20.20.2/24   → FastEthernet0/0.20 (VLAN 20)
10.30.10.2/24   → FastEthernet0/0.10 (VLAN 10)
```

**GUI**

![nautobot](screenshots/ip-addresses.png)

![nautobot](screenshots/ip-addresses-2.png)

**API Python Object**

![nautobot](screenshots/ip-address-object-json.png)

### 2.3 Interface-to-IP Relationships GUI and API Object

The IPAM model maintains explicit relationships between IP addresses and interfaces, enabling automation scripts to query "what IP is on this interface" or "what interface has this IP."

**GUI**

![nautobot](screenshots/interface-ip-address-gui.png)

**API Python Object**

![nautobot](screenshots/interface-to-ip-object-json.png)

---

### 3 pynautobot Python Library

The `pynautobot` library provides Pythonic access to the Nautobot REST API, enabling automation scripts to query and manipulate the SOT programmatically.

**Pulling Location and Device Role in Script**

![nautobot](screenshots/pynautobot-code-snippet.png)

**Pulling Platform, Device Type, and Prefix in Script**

![nautobot](screenshots/pynautobot-code-snippet-2.png)

### 3.1 Automation Use Cases

The structured SOT data enables multiple automation workflows:

1. **Dynamic Inventory Generation:**
   - Query Nautobot to generate Ansible inventory files
   - Filter devices by site, role, or platform
   - Automatically include/exclude devices based on status

2. **Configuration Template Rendering:**
   - Pull interface details (name, description, IP) from Nautobot
   - Pass data to Jinja2 templates for config generation
   - Ensure configurations match the documented SOT

3. **Compliance Validation:**
   - Compare running configs against Nautobot records
   - Detect configuration drift
   - Alert on undocumented changes

4. **Monitoring Integration:**
   - Generate PRTG/Grafana device lists from Nautobot
   - Auto-discover interfaces to monitor
   - Sync IP address inventories

---

## 4. Evidence 

| Capability | Evidence File | What It Demonstrates |
| :--- | :--- | :--- |
| **Device Inventory** | `device-object-json-mia-r2.png` | Complete device object with nested relationships (role, platform, status) |
| | `nautobot-device-list-1.png` | UI view of device inventory across sites |
| **Interface Modeling** | `interface-object-json.png` | Interface object with description, type, and device relationship |
| **IPAM - Prefixes** | `prefixes.png` | Hierarchical prefix structure for all sites |
| **IPAM - Addresses** | `ip-addresses.png` | WAN /30 addressing (172.16.0.0/16 space) |
| | `ip-addresses-2.png` | LAN VLAN addressing (10.x.x.x/24 subnets) |
| **IP-to-Interface Mapping** | `interface-to-ip-object-json.png` | Explicit relationship between IP addresses and interfaces |
| | `ip-address-object-json.png` | IP address object with nested interface reference |
| **API Integration** | `pynautobot-code-snippet.png` | Python code using pynautobot to query Nautobot |
| | `pynautobot-code-snippet-2.png` | Additional automation script examples |
| | `nautobot-json-print-script.png` | Script output showing structured JSON data retrieval |
| **Location Hierarchy** | `location-object-json.png` | Site/location object structure |

---

### What's Next?

With the Network Source of Truth (SOT) fully configured, integrated with pynautobot, and validated, the next step is to explore the broader automation pipelines that leverage this SOT data.

Continue to the next major module to explore the comprehensive automation implementation:
-  **[Automation](../Automation/)** – Python and Ansible automation pipelines, ITSM integration, GitHub Actions CI/CD, and Batfish pre-deployment validation.
