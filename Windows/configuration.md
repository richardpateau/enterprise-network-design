# Windows Infrastructure Configuration Index

## Overview

This document serves as the central configuration index for the Windows and Microsoft 365 infrastructure within the Meridian Financial Services enterprise environment. 

Rather than duplicating detailed steps, this document provides a high-level summary of the configuration workflows, security baselines, and service integrations implemented across the environment. For granular implementation details, testing methodologies, and evidence matrices, please refer to the specific `configuration.md` file within each feature directory.

---

## Configuration Matrix

| Feature Area | Core Configuration Scope |
| :--- | :--- |
| **[01-DHCP](./01-DHCP/configuration.md)** | Centralized IP management, scope/pool configuration, Cisco `ip helper` relay integration, and DORA protocol validation. |
| **[02-DNS-GPO](./02-DNS-GPO/configuration.md)** | Forward/Reverse DNS zones, domain integration, and centralized security baselines (Firewall, ICMP, Password, Account Lockout) via Group Policy. |
| **[03-File-Shares](./03-File-Shares/configuration.md)** | Role-Based Access Control (RBAC) enforcement via Windows Share and granular NTFS permissions. |
| **[04-Logging-SIEM](./04-Logging-SIEM/configuration.md)** | Windows Advanced Audit Policy (logons, lockouts) and centralized log aggregation/visibility via Splunk. |
| **[05-NTP](./05-NTP/configuration.md)** | Time synchronization for Kerberos compliance and log correlation, managed via GPO and verified on Cisco infrastructure. |
| **[06-RDP](./06-RDP/configuration.md)** | Secure remote graphical administration with Network Level Authentication (NLA) enabled. |
| **[07-Microsoft-365](./07-Microsoft-365/configuration.md)** | Cloud identity provisioning, MFA enforcement, administrative role delegation, and SharePoint/OneDrive collaboration services. |

---

## Feature Configuration Summaries

### 01 — Dynamic Host Configuration Protocol (DHCP)
Provides automated, centralized IPv4 address management for enterprise clients.
- **Configuration:** Windows DHCP scopes, address pools, and exclusion ranges.
- **Integration:** Cisco router `ip helper-address` configuration for cross-subnet relay.
- **Validation:** Client IP/gateway/DNS assignment and packet-level DORA exchange analysis via Wireshark.
- 🔗 *See detailed workflow:* [`01-DHCP/configuration.md`](./01-DHCP/configuration.md)

### 02 — DNS & Group Policy (GPO)
Delivers reliable name resolution and automated, centralized security management for all domain-joined endpoints.
- **Configuration:** Forward and Reverse lookup zones, PTR records, and domain joining.
- **Security Baselines:** Windows Defender Firewall rules, controlled ICMP allowances, strict password complexity, and account lockout thresholds.
- **Validation:** Client-side DNS resolution testing and `gpresult` verification of policy application.
- 🔗 *See detailed workflow:* [`02-DNS-GPO/configuration.md`](./02-DNS-GPO/configuration.md)

### 03 — File Shares & Access Control
Demonstrates the Principle of Least Privilege through differentiated Windows file-sharing and NTFS permissions.
- **Configuration:** Dedicated file shares with granular NTFS access control lists (ACLs).
- **Validation:** Positive testing (Network Admin: Read/Write/Create/Delete) and negative testing (Standard 802.1X User: Read-Only, Write/Create Denied).
- 🔗 *See detailed workflow:* [`03-File-Shares/configuration.md`](./03-File-Shares/configuration.md)

### 04 — Logging & SIEM Integration
Ensures security visibility and audit compliance by capturing authentication events and aggregating them centrally.
- **Configuration:** Windows Advanced Audit Policy for successful/failed logons and account lockouts.
- **Integration:** Forwarding of Windows Event Logs to Splunk for centralized visibility.
- **Validation:** Intentional generation of failed logins and lockouts, verified in both Windows Event Viewer and Splunk search.
- 🔗 *See detailed workflow:* [`04-Logging-SIEM/configuration.md`](./04-Logging-SIEM/configuration.md)

### 05 — Network Time Protocol (NTP)
Maintains strict time synchronization, a critical dependency for Active Directory Kerberos authentication and accurate SIEM log correlation.
- **Configuration:** Centralized NTP client policy deployed via Group Policy.
- **Validation:** PowerShell `w32tm` verification on Windows endpoints and `show ntp associations` verification on core Cisco routers.
- 🔗 *See detailed workflow:* [`05-NTP/configuration.md`](./05-NTP/configuration.md)

### 06 — Remote Desktop Protocol (RDP)
Enables secure, encrypted remote graphical administration of Windows infrastructure.
- **Configuration:** Enabling Remote Desktop service with Network Level Authentication (NLA) enforced.
- **Validation:** Successful establishment of a remote session from an administrative client.
- 🔗 *See detailed workflow:* [`06-RDP/configuration.md`](./06-RDP/configuration.md)

### 07 — Microsoft 365 Administration
Extends the on-premises identity model into the cloud, providing secure productivity and collaboration services.
- **Identity & Security:** User provisioning, licensing, MFA enforcement, and administrative role delegation (RBAC).
- **Productivity:** OneDrive administration and Exchange Online automatic reply configuration.
- **Collaboration:** SharePoint site creation, document library setup, and version-controlled document recovery testing.
- **Compliance:** Review of Azure AD/M365 Sign-In logs and the Unified Audit Log for activity tracking.
- 🔗 *See detailed workflow:* [`07-Microsoft-365/configuration.md`](./07-Microsoft-365/configuration.md)

---

## Documentation Standard

Each Windows feature is documented independently using a consistent, two-tier structure to separate design intent from implementation proof:

```text
Feature/
├── README.md             # Architecture, objectives, and scope
├── configuration.md      # Detailed workflow and evidence 
└── screenshots/          # Curated configuration and validation evidence
```

---

## Implementation Dependency Model

The Windows infrastructure is deployed in a logical, layered sequence, where foundational services must be operational before dependent services can be configured:

![Read ME](screenshots/windows-config-visio.png)
