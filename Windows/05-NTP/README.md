# Windows NTP & Time Synchronization

## Overview

This section documents the implementation of Network Time Protocol (NTP) within the Meridian Financial Services environment. 

Accurate time synchronization is a **critical foundational requirement** for enterprise networks. It is strictly required for:
- **Active Directory Kerberos Authentication** (fails if time drift exceeds 5 minutes)
- **Log Correlation** across Windows Events, Cisco Syslogs, and the Splunk SIEM
- **Certificate Validation** and PKI operations
- **Scheduled Task Execution** and backup consistency

The implementation utilizes Group Policy Objects (GPO) to centrally manage time synchronization for all domain-joined Windows clients, while Cisco network infrastructure is independently verified for NTP status and associations.

---

## Architecture

![NTP](screenshots/ntp-visio.png)

---

## Design Objectives

- **Centralized Management:** Leverage Group Policy to push NTP settings to all domain endpoints, preventing local configuration drift and ensuring consistency.
- **Kerberos Compliance:** Ensure all domain-joined machines remain within the strict 5-minute time drift tolerance required for Active Directory authentication.
- **Cross-Platform Consistency:** Validate that both Windows endpoints and Cisco network infrastructure are synchronized to reliable time sources.
- **Audit Readiness:** Provide verifiable proof of time synchronization configuration for compliance and security audits.

---

## Implementation Scope

### Windows Infrastructure (GPO)
- Creation of the "Meridian - Domain Time Synchronization" GPO.
- Configuration of the "Configure Windows NTP Client" policy settings.
- Client-side verification using PowerShell (`w32tm /query /status`).

![NTP](screenshots/ntp-gpo-added.png)

### Network Infrastructure (Cisco IOS)
- Verification of NTP status and associations on core routers (HQ-R1, HQ-R2).
- Validation of stratum levels and synchronization sources.

![NTP](screenshots/r1-sh-ntp-status.png)

---

## Documentation Structure

| Document | Purpose |
| :--- | :--- |
| `README.md` | Architecture, design objectives, and implementation scope. |
| `configuration.md` | GPO settings, Cisco IOS verification, and evidence |
| `screenshots/` | Curated evidence of GPO configuration, client verification, and router status. |

---

## Scope & Boundaries

This section documents **Windows NTP client configuration via GPO and Cisco NTP status verification**. 

It demonstrates the successful configuration and validation of time synchronization across the enterprise. It does not define the complete NTP server hierarchy beyond what is demonstrated by the evidence.

---

## Related Documentation

- **Active Directory & GPO:** `Windows/02-DNS-GPO/`
- **Logging & SIEM:** `Windows/04-Logging-SIEM/` (Relies on accurate NTP for log timestamps)
