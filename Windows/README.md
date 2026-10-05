Here is the polished, portfolio-ready version of your top-level `Windows/README.md`. 

I have elevated the language to emphasize **enterprise infrastructure standards, security baselines, and centralized management**, ensuring it perfectly matches the senior-engineer tone of the rest of your portfolio.

***

# Windows Infrastructure & Microsoft 365

## Overview

This section documents the core Windows infrastructure and Microsoft 365 cloud services implemented for the Meridian Financial Services enterprise environment. 

The environment provides centralized identity management, directory services, security policy enforcement, remote administration, time synchronization, and collaborative productivity tools. The implementation is modularized into distinct feature areas, allowing for independent review of configuration, security controls, and functional validation evidence.

---

## Architecture

![Read ME](screenshots/windows-readme-visio.png)

---

## Feature Areas

### 01 — Dynamic Host Configuration Protocol (DHCP)
Provides centralized, dynamic IPv4 address management for enterprise clients.
- **Key Implementations:** Windows DHCP scope/pool configuration, active lease management, Cisco router `ip helper` relay integration, and packet-level DORA validation via Wireshark.
- **Documentation:** [`01-DHCP/`](./01-DHCP/)

### 02 — DNS & Group Policy (GPO)
Delivers reliable name resolution and centralized, automated security management for all domain-joined endpoints.
- **Key Implementations:** Forward/Reverse lookup zones, PTR records, Windows Defender Firewall rules, ICMP allowances, and strict Password/Account Lockout security baselines.
- **Documentation:** [`02-DNS-GPO/`](./02-DNS-GPO/)

### 03 — File Shares & Access Control
Demonstrates Role-Based Access Control (RBAC) and the Principle of Least Privilege via Windows file sharing and NTFS permissions.
- **Key Implementations:** Differentiated access testing proving Network Administrators have full control, while standard 802.1X users are strictly limited to read-only access.
- **Documentation:** [`03-File-Shares/`](./03-File-Shares/)

### 04 — Logging & SIEM Integration
Ensures security visibility and audit compliance by capturing authentication events and aggregating them centrally.
- **Key Implementations:** Windows Advanced Audit Policy (failed/successful logons, account lockouts) and successful ingestion/visibility of these events in Splunk.
- **Documentation:** [`04-Logging-SIEM/`](./04-Logging-SIEM/)

### 05 — Network Time Protocol (NTP)
Maintains strict time synchronization, a critical dependency for Active Directory Kerberos authentication and accurate SIEM log correlation.
- **Key Implementations:** Centralized NTP client configuration via Group Policy, PowerShell validation on Windows endpoints, and NTP association verification on Cisco routers.
- **Documentation:** [`05-NTP/`](./05-NTP/)

### 06 — Remote Desktop Protocol (RDP)
Enables secure, encrypted remote graphical administration of Windows infrastructure.
- **Key Implementations:** Service configuration with Network Level Authentication (NLA) and functional validation of successful remote sessions.
- **Documentation:** [`06-RDP/`](./06-RDP/)

### 07 — Microsoft 365 Administration
Extends the on-premises identity model into the cloud, providing secure productivity and collaboration services.
- **Key Implementations:** Cloud user provisioning, licensing, MFA enforcement, administrative role delegation (RBAC), OneDrive/Exchange configuration, and SharePoint site creation with version-controlled document recovery.
- **Documentation:** [`07-Microsoft-365/`](./07-Microsoft-365/)

---

## Repository Structure

```text
Windows/
├── README.md
│
├── 01-DHCP/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
│
├── 02-DNS-GPO/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
│
├── 03-File-Shares/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
│
├── 04-Logging-SIEM/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
│
├── 05-NTP/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
│
├── 06-RDP/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
│
└── 07-Microsoft-365/
    ├── README.md
    ├── configuration.md
    └── screenshots/
```

---

## Documentation Standard

Each Windows feature is documented independently using a consistent, two-tier structure to separate design intent from implementation proof:

1. **`README.md`** — Defines the architecture, design objectives, security considerations, and implementation scope.
2. **`configuration.md`** — Details the specific configuration steps, testing methodology, and includes an **Evidence Matrix** mapping screenshots to the specific controls they validate.

Screenshots and media files are strictly contained within the `screenshots/` subdirectory of each feature to maintain a clean, professional repository structure.

---

## Infrastructure Role

The Windows and Microsoft 365 environments serve as the foundational identity, directory, and productivity layer for the broader Meridian enterprise network. They integrate seamlessly with the network routing, Cisco ISE security policies, and PRTG monitoring systems to deliver a cohesive, secure, and manageable enterprise IT ecosystem.

***
