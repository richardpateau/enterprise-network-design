# Windows NTP Implementation & Validation

## Overview

This document details the configuration of Network Time Protocol (NTP) across the Meridian environment. It covers the Group Policy configuration for Windows endpoints and the corresponding verification of NTP status on Cisco network infrastructure.

---

## 1. Windows GPO Configuration

To ensure all domain-joined computers synchronize time correctly, a dedicated Group Policy Object was created and linked to the appropriate Organizational Unit.

### 1.1 GPO Creation
A GPO named **"Meridian - Domain Time Synchronization"** was created to centrally manage NTP settings.

![NTP](screenshots/gpo-overview.png)

![NTP](screenshots/ntp-gpo-added.png)

### 1.2 NTP Client Policy Settings
Within the GPO, the "Configure Windows NTP Client" policy was enabled. This configures the Windows Time service (`w32time`) to synchronize with the domain hierarchy (NT5DS mode) or a specific external source.

![NTP](screenshots/ntp-client-config.png)

---

## 2. Client-Side Verification

After the GPO is applied, the Windows Time service must be verified on the endpoint to confirm it is receiving the correct policy and synchronizing successfully.

### 2.1 Policy Mapping Verification
PowerShell was used to confirm that the NTP GPO was successfully mapped to the Windows 10 client.

![NTP](screenshots/policy-mapped.png)

### 2.2 Time Service Status
The Windows 10 client was verified to have successfully applied the NTP configuration.

### 2.3 Detailed PowerShell Validation
Additional PowerShell commands (`w32tm /query /status`) were executed to verify the detailed state of the Windows Time service, including stratum level and last sync time.

![NTP](screenshots/windows-successful-sync.png)

---

## 3. Cisco Network Infrastructure Verification

To ensure network devices have accurate timestamps for Syslog and debugging, NTP status was verified on core routers.

### 3.1 HQ-R1 NTP Status
NTP status and associations were verified on HQ-R1 to confirm synchronization.

![NTP](screenshots/r1-sh-ntp-status.png)

### 3.2 HQ-R2 NTP Status
NTP status and associations were verified on HQ-R2 to confirm synchronization.

![NTP](screenshots/r2-sh-ntp-status.png)

---

## 4. Evidence Matrix

| Verification Stage | Evidence File | What It Proves |
| :--- | :--- | :--- |
| **Architecture** | `ntp-visio.png` | NTP architecture and workflow diagram. |
| **GPO Configuration** | `gpo-overview.png` | NTP Group Policy overview and structure. |
| | `ntp-gpo-added.png` | NTP GPO successfully created and linked. |
| | `ntp-client-config.png` | Windows NTP client policy settings configured. |
| **Client Application** | `policy-mapped.png` | Windows 10 client successfully mapped NTP policy. |
| | `windows-10-ntp.png` | Windows 10 NTP configuration confirmed. |
| **Network Device Sync** | `r1-sh-ntp-status.png` | HQ-R1 NTP status and associations verified. |
| | `r2-sh-ntp-status.png` | HQ-R2 NTP status and associations verified. |

---

## 5. Scope & Boundaries

This section documents **Time Synchronization via GPO and Cisco IOS verification**.

**Not covered here:**
- General Group Policy architecture (covered in `02-DNS-GPO/`)
- Syslog server configuration (covered in `04-Logging-SIEM/`)
