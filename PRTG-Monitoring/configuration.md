# PRTG Monitoring Implementation & Validation Model

## Overview

This document details the configuration model used to deploy proactive monitoring across the Meridian environment. It covers device onboarding, sensor deployment, threshold configuration, and the validation of the automated alerting workflow.

---

## 1. Device Onboarding & SNMPv3 Security

To ensure secure monitoring, Cisco infrastructure is polled exclusively via **SNMPv3** (providing authentication and encryption), rather than the insecure SNMPv1/v2c.

**Implementation:**
1. Cisco devices are configured with an SNMPv3 user (Auth: SHA, Priv: AES).
2. The device is added to PRTG using its management IP.
3. PRTG device settings are updated with the corresponding SNMPv3 credentials.

![PRTG](screenshots/r1-sh-run-include-snmp.png)

![PRTG](screenshots/prtg-add-new-device.png)

![PRTG](screenshots/prtg-snmp-v3.png)

---

## 2. Network Performance & Health Sensors

Baseline health sensors are auto-discovered or manually added to provide a high-level view of device stability.

**Configured Sensors:**
- **Cisco Health:** Overall device status.
- **CPU & Memory:** Custom thresholds configured (e.g., Warning at 70%, Error at 90%) to detect resource exhaustion before it impacts forwarding.
- **System Uptime:** Alerts triggered if the uptime counter resets, indicating an unexpected reboot.

![PRTG](screenshots/r1-sensor-overview.png)

![PRTG](screenshots/cpu-alert-limit.png)

![PRTG](screenshots/system-uptime.png)

---

## 3. Interface & Traffic Analytics

Critical interfaces (e.g., WAN uplinks, core trunks) are monitored for both performance and physical layer health.

**Configured Sensors:**
- **SNMP Traffic:** Monitors Inbound/Outbound bandwidth utilization.
- **Errors & Discards:** Dedicated sensors for Input/Output Errors and Discards. 
- **Thresholds:** Alerts are configured to trigger on sustained discards, which often indicate micro-bursts or duplex mismatches.

![PRTG](screenshots/interface-discards-in-out.png)

---

## 4. Availability & Latency Monitoring

Reachability is validated using advanced Ping sensors that go beyond simple up/down status.

**Configured Sensors:**
- **Ping:** Baseline ICMP reachability.
- **Latency & Packet Loss:** Thresholds configured to alert on degraded performance (e.g., >50ms latency or >1% packet loss) *before* the link goes completely down.

![PRTG](screenshots/r1-ping-v2.png)

---

## 5. Windows Infrastructure Monitoring

Native PRTG Windows sensors are deployed to monitor critical server roles without requiring additional agents.

**Configured Sensors:**
- **Service Monitoring:** Active Directory, DNS, and DHCP service status.
- **Remote Access:** RDP port (3389) availability.
- **Event Log:** Application Event Log sensor filtered to trigger *only* on "Error" level events.
- **Disk Space:** Free disk space monitoring with a threshold (e.g., <15% free) to prevent storage-related outages.

![PRTG](screenshots/windows-sensor-overview.png)

---

## 6. Alerting & ITSM Integration Workflow

Sensors are linked to **Notification Triggers** to automate the response to failures. 

**Workflow Validation:**
1. **Condition:** A monitored threshold is breached (e.g., Interface Shutdown, CPU Spike, DNS Service Stop).
2. **Trigger:** PRTG evaluates the notification trigger associated with the sensor/device.
3. **Action:** PRTG simultaneously updates the Dashboard status, sends an Email Alert, and generates an ITSM Ticket.

---

## 7. Functional Validation & Evidence Matrix

The monitoring implementation was rigorously validated through intentional fault injection. The following evidence matrix maps the tested failure scenarios to the captured artifacts.

### 7.1 Network Fault Injection
- **CPU/Memory:** Simulated high utilization to verify threshold alerts and ticket generation.
- **Interface Down:** Administratively shut down a monitored interface to verify immediate "Down" status, email alert, and ticket creation.
- **Traffic/Discards:** Generated traffic to hit utilization limits and verified discard alerting.
- **Latency/Packet Loss:** Introduced artificial network degradation to validate advanced ping sensor alerts.

**Example: CPU alert limit**

![PRTG](screenshots/cpu-alert-limits.png)

**CPU notification trigger**

![PRTG](screenshots/cpu-notification-trigger.png)

**CPU Intentional Overloading via ping**

![PRTG](screenshots/intentional-cpu-overloading.png)

**Ticket Created**

![PRTG](screenshots/cpu-ticket.png)

**Email Received**

![PRTG](screenshots/cpu-email.png)

**Example: Packet loss alert limits**

![PRTG](screenshots/packet-loss-alert-config.png)

**Packet loss trigger via Alpine Linux**

![PRTG](screenshots/packet-loss-intentional-trigger.png)

**Packet loss ticket created**

![PRTG](screenshots/packet-loss-ticket.png)

**Packet loss email created**

![PRTG](screenshots/packet-loss-email.png)

### 7.2 Windows Fault Injection
- **Service Failure:** Intentionally stopped AD, DNS, DHCP, and RDP services to verify rapid detection and alerting.
- **Event Log:** Used PowerShell to generate a fake Application Error to validate Event Log parsing.
- **Disk Space:** Simulated a low-disk-space condition to verify storage threshold alerting.

**Example: Active Directory Notifcation Trigger**

![PRTG](screenshots/ad-notification-trigger.png)

**Powershell: Intentional AD shutdown**

![PRTG](screenshots/ad-intentional-shutdown.png)

**AD Ticket Creation**

![PRTG](screenshots/ad-ticket.png)

**AD Email Creation**

![PRTG](screenshots/ad-email.png)

**Example: DHCP Notifcation Trigger**

![PRTG](screenshots/dhcp-notifcation-trigger.png)

**Powershell: Intentional DHCP shutdown**

![PRTG](screenshots/dhcp-intentional-shutdown.png)

**DHCP Ticket Creation**

![PRTG](screenshots/dhcp-ticket.png)

**DHCP Email Creation**

![PRTG](screenshots/dhcp-email.png)
---

## 8. Evidence Repository

Curated screenshots validating this implementation are stored in:
`PRTG/screenshots/` *(or `PRTG Router Monitoring/screenshots/` depending on your folder name)*

**Evidence Checklist:**

**SNMPv3 & Device Onboarding:**
- [x] `r1-sh-run-include-snmp.png` (Proof of Cisco device SNMPv3 configuration)
- [x] `pftg-snmp-v3.png` (Proof of PRTG SNMPv3 credential setup)
- [x] `prtg-add-new-device.png` (Proof of HQ-R1 device onboarding)

**Network Health & Interface Monitoring:**
- [x] `cpu-alert-limits.png` (Proof of CPU threshold configuration)
- [x] `intentional-cpu-overloading.png` (Proof of CPU fault injection)
- [x] `interface-discards-in-out.png` (Proof of interface error/discard monitoring)
- [x] `packet-lost-alert-config.png` / `packet-loss-intentional-trigger.png` (Proof of packet loss monitoring and trigger)
- [x] `r1-ping-v2.png` (Proof of baseline ping/availability monitoring)
- [x] `system-uptime.png` (Proof of system uptime sensor)

**Windows Infrastructure Monitoring:**
- [x] `windows-sensor-overview.png` (Proof of Windows sensor deployment)
- [x] `ad-intentional-shutdown.png` (Proof of Active Directory fault injection)
- [x] `dhcp-intentional-shutdown.png` (Proof of DHCP fault injection)

**Alerting, Notifications & ITSM Integration:**
- [x] `email-notification-config.png` (Proof of email notification setup)
- [x] `ticket-config.png` (Proof of ticket notification setup)
- [x] `notification-template-overview.png` (Proof of notification template)
- [x] `cpu-ticket.png` / `cpu-email.png` (Proof of CPU alert triggering email and ticket)
- [x] `ad-ticket.png` / `ad-email.png` (Proof of AD alert triggering email and ticket)
- [x] `dhcp-ticket.png` / `dhcp-email.png` (Proof of DHCP alert triggering email and ticket)
- [x] `PING TEST PACKET LOSS TICKET CREATED.png` (Proof of packet loss ticket generation)

**Architecture & Overview:**
- [x] `prtg-visio.png` / `prft-alerting-visio.png` (Proof of monitoring architecture)
- [x] `r1-sensor-overview.png` (Proof of comprehensive sensor scale on HQ-R1)
