# Monitoring Pipeline Configuration & Automation

## Overview

This document details the configuration of the Meridian monitoring pipeline, focusing on the secure collection of telemetry via SNMPv3, the deployment of Telegraf agents, and the rigorous validation of dashboard accuracy against live network events.

---

## Phase 1: Secure Telemetry Collection (SNMPv3)

To ensure monitoring traffic is secure, SNMPv3 was configured across all Cisco devices with authentication and privacy enabled.

**Ansible Automation:**  
SNMPv3 users, groups, and access control lists were deployed consistently using Ansible playbooks, ensuring configuration compliance across the fleet.  

**Ansible Automation:**  
The deployment followed a strict sequence to ensure security compliance:
1. `02_base_config.yml`: Established baseline management access.
2. `04_configure_snmpv3_usernames.yml` & `05_configure_asa_snmpv3.yml`: Deployed secure SNMPv3 users and groups.
3. `03_enable_telegraf_snmp-acl.yml`: Restricted SNMP polling strictly to the Telegraf server IP via ACLs.

![Grafana](screenshots/snmpv3-playbook.png)

![Grafana](screenshots/snmpv3-playbook-results.png)

## Phase 2: Telegraf Agent Deployment

Telegraf was deployed as the data collection agent, configured to poll the network devices via SNMPv3 and write the metrics to InfluxDB.

**Ansible Automation:**  
The Telegraf configuration and service deployment were automated via Ansible, eliminating manual configuration drift.  

![Grafana](screenshots/telegraf-anisble-playbook.png)

![Grafana](screenshots/telegraf-playbook-results.png)

**Jinja2**

![Grafana](screenshots/jinja-template.png)

**Result of playbook** 

![Grafana](screenshots/template-result.png)

---

## Phase 3: Dashboard Validation & Testing

The core of this implementation is proving the dashboard accurately reflects network reality. The following controlled tests were performed:

### 3.1 HSRP Gateway Failover
An intentional interface shutdown was performed on the active HSRP router. The dashboard updated to show the standby router assuming the Active role.  

![Grafana](screenshots/hsrp-test-baseline.png)

![Grafana](screenshots/hsrp-intentional-shutdown-r1.png)

![Grafana](screenshots/hsrp-panel-during-failure.png)


**Please enlarge for clearer video**

https://github.com/user-attachments/assets/ad01abb8-8132-4b85-8e25-184b26ef6647

### 3.2 ISP Connectivity Failure
The primary ISP-A path was deliberately failed. The Grafana IP SLA panel immediately reflected the loss of reachability.  

![Grafana](screenshots/isp-panel-before-failure.png)

![Grafana](screenshots/isp-intentional-fail.png)

![Grafana](screenshots/isp-panel-during-failure.png)

**Please enlarge for clearer video**

https://github.com/user-attachments/assets/c9854e59-7ff9-44e1-9842-84976e060ad2

### 3.3 OSPF Neighbor Monitoring
A routing link was shut down to verify OSPF adjacency monitoring. The dashboard correctly showed the neighbor state transitioning from FULL to DOWN, matching the CLI output.  

![Grafana](screenshots/ospf-panel-before-failure.png)

![Grafana](screenshots/ospf-intentional-failure-r1.png)

![Grafana](screenshots/ospf-panel-during-failure.png)

**Please enlarge for clearer video**

https://github.com/user-attachments/assets/cd50167f-3b7e-4b0a-a045-076df29ae1f4

### 3.4 Site-to-Site VPN Verification
Grafana IPsec tunnel counters were cross-referenced with the Cisco ASA CLI to ensure data accuracy.  

![Grafana](screenshots/ip-sec-panel.png)

![Grafana](screenshots/ip-sec-cli.png)

### 3.5 DMZ Web Server Health
An HTTP health check panel was implemented to monitor the DMZ web server's response time, distinguishing between basic ICMP reachability and actual application-layer availability.


![Grafana](screenshots/dmz-server.png)

![Grafana](screenshots/dmz-server-oid.png)


---

## Evidence

| Verification Stage | Evidence File | What It Proves |
| :--- | :--- | :--- |
| **Dashboard Overview** | `dashboard-overview-1.png` to `3.png` | Complete NOC dashboard layout and panels. |
| | `grafana.png` | Grafana data source integration (InfluxDB). |
| **Ansible Automation** | `snmpv3-playbook.png` & `snmpv3-playbook-results.png` | Secure SNMPv3 credentials deployed via Ansible. |
| | `hq-fw-snmp-playbook results successful.png` | Firewall-specific SNMPv3 playbook execution. |
| | `telegraf-anisble-playbook.png` & `telegraf-playbook-results.png` | Automated Telegraf agent deployment. |
| | `jinja-template.png` & `template-result.png` | Dynamic configuration generation using Jinja2. |
| **HSRP Validation** | `hsrp-test-baseline.png` | Dashboard accurately reflects normal HSRP state. |
| | `hsrp-panel-during-failure.png` | Dashboard updates to reflect HSRP role change. |
| | `hsrp-intentional-shutdown-r1.png` | CLI proof of the controlled failure trigger. |
| | `videos/hsrp-video.mp4` | Live video proof of dashboard reaction to failover. |
| **ISP Validation** | `isp-panel-before-failure.png` | Dashboard baseline for ISP-A IP SLA reachability. |
| | `isp-panel-during-failure.png` | Dashboard accurately reflects ISP path failure. |
| | `isp-intentional-fail.png` | CLI proof of the controlled ISP failure trigger. |
| | `videos/isp-video.mp4` | Live video proof of dashboard reaction to ISP loss. |
| **OSPF Validation** | `ospf-panel-before-failure.png` | Dashboard baseline showing OSPF neighbors in FULL state. |
| | `ospf-panel-during-failure.png` | Dashboard accurately reflects OSPF adjacency loss. |
| | `ospf-intentional-failure-r1.png` | CLI proof of the routing link shutdown. |
| | `videos/ospf-video.mp4` | Live video proof of dashboard reaction to OSPF failure. |
| **VPN Validation** | `ip-sec-panel.png` | Grafana IPsec tunnel counters and state. |
| | `ip-sec-cli.png` | CLI verification (`show crypto ipsec sa`) matching Grafana. |
| **Application Health** | `dmz-server.png` | HTTP response time and availability for DMZ web server. |
| | `dmz-server-oid.png` | SNMP OID mapping for application-layer monitoring. |
---
