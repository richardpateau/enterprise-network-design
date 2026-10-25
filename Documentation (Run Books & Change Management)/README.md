# Documentation: Run Books & Change Management

## Overview

This directory contains the standardized operational documentation for the Meridian Financial Services enterprise network. 
---

## Change Management Protocol

1. **Risk Assessment:** Every Change Request (CR) defines the risk profile, scope, and estimated downtime.
2. **Pre-Validation:** Baseline states are captured before any modifications occur.
3. **Step-by-Step Execution:** Clear, copy-paste-ready configuration blocks prevent human error during maintenance windows.
4. **Post-Validation:** Success criteria are explicitly defined and tested immediately after implementation.
5. **Backout/Rollback Plan:** Every CR includes a tested, immediate rollback procedure to restore service in the event of failure.

---

## Document Inventory

### Change Requests (CR)
Formal proposals for network modifications, complete with justification, risk analysis, and rollback procedures.

| Document | Title | Risk Profile | Objective |
| :--- | :--- | :---: | :--- |
| [`CR-001-HSRP-to-VRRP.md`](CR-001-HSRP-to-VRRP.md) | HSRP to VRRP Migration | Medium | Migrate First-Hop Redundancy to a vendor-agnostic standard. |
| [`CR-002-OS-UPGRADE.md`](CR-002-OS-UPGRADE.md) | Automated OS Upgrade | Medium | Safely upgrade physical switch firmware via Ansible and TFTP. |
| [`CR-003-SNMPv2-to-SNMPv3.md`](CR-003-SNMPv2-to-SNMPv3.md) | SNMPv2 to SNMPv3 Migration | Medium | Harden network monitoring traffic with authentication and encryption. |
| [`CR-004-8021X.md`](CR-004-8021X.md) | 802.1X NAC Deployment | High | Roll out identity-based Network Access Control to edge switches. |
| [`CR-005-PRTG-Threshold-Change.md`](CR-005-PRTG-Threshold-Change.md) | PRTG CPU Threshold Change | Low | Optimize monitoring alerts to reduce NOC alert fatigue. |

### Run Books (RB)
Standardized, step-by-step operational procedures for deploying or troubleshooting specific network services.

| Document | Title | Scope | Objective |
| :--- | :--- | :--- | :--- |
| [`RB-001-Site-to-Site-VPN.md`](RB-001-Site-to-Site-VPN.md) | Site-to-Site IPsec VPN | HQ to Ashburn DR | Deploy redundant, encrypted IKEv2 tunnel between data centers. |
| [`RB-002-Remote-Access-VPN.md`](RB-002-Remote-Access-VPN.md) | Remote Access VPN | End Users | Configure AnyConnect with Microsoft Entra ID SAML SSO and MFA. |
| [`RB-003-Azure-Site-to-Site-VPN.md`](RB-003-Azure-Site-to-Site-VPN.md) | Azure Hybrid Connectivity | On-Prem to Azure | Establish BGP-enabled Site-to-Site VPN to Azure Virtual Network Gateway. |
| [`RB-004-ASA-HA-Firewall.md`](RB-004-ASA-HA-Firewall.md) | ASA High Availability | HQ Firewalls | Configure Active/Standby failover with stateful connection replication. |
| [`RB-005-Cisco-ISE-Policy.md`](RB-005-Cisco-ISE-Policy.md) | Cisco ISE Policy Creation | Network Access | Define and apply 802.1X/MAB authorization profiles for VLAN assignment. |

### Templates
Reusable frameworks to ensure consistency across all future operational documentation.
- [`CR-Template.md`](CR-Template.md) — Standardized Change Request template.
- [`runbook-template.md`](runbook-template.md) — Standardized Run Book template.

---

### Return to Main Portfolio

- **[Enterprise Network Design & Implementation (Root)](../../README.md)**
