# Meridian Enterprise Network Operations Documentation

**Author:** Richard Pateau  
**Environment:** Meridian Enterprise Lab (HQ, Ashburn Branch & Microsoft Azure Hybrid Core)

This repository showcases production-grade **Configuration Runbooks** and **Change Management Plans** engineered for the Meridian multi-site enterprise network. Rather than raw configuration dumps, these documents demonstrate end-to-end network engineering discipline, covering architecture design, pre-change baselining, CLI/GUI implementation, packet and session-level validation, and deterministic rollback planning.

---

## Core Engineering Capabilities Demonstrated

* **Hybrid Cloud & Perimeter Security:** Engineered policy-based and route-based (VTI) IKEv2 IPsec VPNs across Cisco ASA firewalls and Microsoft Azure VPN Gateways, alongside Stateful Active/Standby High Availability failover.
* **Identity-Driven Access Control (Zero Trust / NAC):** Integrated Cisco AnyConnect (Secure Client) with **Microsoft Entra ID SAML SSO & Conditional Access MFA**, and deployed **Cisco ISE 802.1X / MAB** authentication tied to Active Directory (`meridian.local`) with dynamic VLAN assignment.
* **Network Automation & Source of Truth:** Built automated Cisco Catalyst OS upgrade workflows driven by **Ansible** and **Nautobot** dynamic inventory, incorporating Git linting and `--check` dry-run validation.
* **Protocol Modernization & Hardening:** Executed standards-based migrations from Cisco-proprietary HSRP to VRRP and hardened monitoring infrastructure from SNMPv2 to authenticated SNMPv3 across PRTG and Grafana (Telegraf).
* **Operational Governance:** Authored standardized Runbook and Change Request frameworks enforcing risk profiling, downtime estimation, pre/post-implementation verification, and tested backout procedures.

---

## Implementation Runbooks (Architecture & Provisioning)

Each runbook documents a complete service deployment from prerequisites through live verification (`show` outputs, SA counters, live logs, and packet captures).

| ID | Document | Platforms & Protocols | What Was Built & Validated |
| :--- | :--- | :--- | :--- |
| **RB-CFG-001** | [RB-001-Site-to-Site-VPN.md](./RB-001-Site-to-Site-VPN.md) | Cisco ASA (`HQ-FW-1`, `ASH-FW-1`), IKEv2/IPsec | Deployed a site-to-site IKEv2 tunnel (AES-256 / SHA-256 / DH Group 14) with crypto maps, interesting traffic ACLs, and identity NAT exemption, verified via SA counters and Wireshark ESP/ISAKMP inspection. |
| **RB-CFG-002** | [RB-002-Remote-Access-VPN.md](./RB-002-Remote-Access-VPN.md) | Cisco ASA (`HQ-FW-1`), AnyConnect, Microsoft Entra ID | Implemented remote-access VPN with external-browser SAML 2.0 authentication against Entra ID, Conditional Access MFA, Let's Encrypt/Azure trustpoints, split-tunneling, and NAT exemption. |
| **RB-CFG-003** | [RB-003-Azure-Site-to-Site-VPN.md](./RB-003-Azure-Site-to-Site-VPN.md) | Cisco ASA (`HQ-FW-1`), Microsoft Azure (VNet, VNG, LNG) | Provisioned Azure East US networking (`Meridian-VNet`, `VpnGw2AZ`, Local Network Gateway) and terminated a route-based IKEv2 VTI (`Tunnel100`) back to on-premises HQ. |
| **RB-CFG-004** | [RB-004-ASA-HA-Firewall.md](./RB-004-ASA-HA-Firewall.md) | Cisco ASA 9.24.x (`HQ-FW-1`, `HQ-FW-2`) | Configured Active/Standby stateful failover over a dedicated `GigabitEthernet0/5` link with dual-stack IPv4/IPv6 active and standby interface addressing. |
| **RB-CFG-005** | [RB-005-Cisco-ISE-Policy.md](./RB-005-Cisco-ISE-Policy.md) | Cisco ISE, Active Directory (`meridian.local`), RADIUS | Onboarded network access devices into ISE, integrated AD identity groups, and authored 802.1X authorization profiles for dynamic VLAN enforcement. |

---

## Change Management Plans (Migrations & Maintenance)

Each Change Request illustrates structured risk management, live verification, and full backout syntax for production maintenance windows.

| CR # | Document | Risk / Impact | Scope & Engineering Execution |
| :--- | :--- | :--- | :--- |
| **CR-001** | [CR-001-HSRP-to-VRRP.md](./CR-001-HSRP-to-VRRP.md) | Medium / < 5 min | Migrated default-gateway redundancy on `HQ-R1` and `HQ-R2` (`f0/0.10`) from HSRP to open-standard VRRP to eliminate vendor lock-in. |
| **CR-002** | [CR-002-OS-UPGRADE.md](./CR-002-OS-UPGRADE.md) | Medium / ~20 min per switch | Automated Catalyst 2960S IOS upgrades (`15.2(2)E8` → `15.2(2)E9`) via Ansible (`os_upgrade.yml`) and Nautobot inventory with dry-run verification and boot-variable rollback. |
| **CR-003** | [CR-003-SNMPv2-to-SNMPv3.md](./CR-003-SNMPv2-to-SNMPv3.md) | Medium / Zero downtime | Migrated Core, Distribution, and Access devices from cleartext SNMPv2 communities to ACL-restricted SNMPv3 (`auth sha`) integrated with PRTG and Telegraf/Grafana. |
| **CR-004** | [CR-004-8021X.md](./CR-004-8021X.md) | High / Zero downtime | Rolled out `aaa new-model`, RADIUS integration with Cisco ISE, and `multi-domain` 802.1X/MAB port controls across access switches with full authentication session validation. |
| **CR-005** | [CR-005-PRTG-Threshold-Change.md](./CR-005-PRTG-Threshold-Change.md) | Medium / Zero downtime | Tuned PRTG CPU load warning/error thresholds (80% / 90%) on `HQ-R1` and validated alerting via simulated threshold triggers to reduce NOC alert fatigue. |

---

## Standardized Documentation Frameworks

To ensure consistency and auditability across all operational work, this repository also includes the custom templates created for these workflows:

* **[runbook-template.md](./runbook-template.md)** — Baseline structure for provisioning SOPs, including Source of Truth (Nautobot/NetBox) checks, IPAM validation, and verification commands.
* **[CR-Template.md](./CR-Template.md)** — Change governance template capturing business justification, risk profile, downtime estimates, pre/post-checks, and rollback syntax.

---

## Technologies & Platforms

| Domain | Stack |
| :--- | :--- |
| **Routing & Switching** | Cisco IOS / IOS-XE, HSRP, VRRP, OSPF, 802.1X, MAB, SNMPv3 |
| **Firewalls & VPN** | Cisco ASA (Active/Standby HA, IKEv2 S2S, Route-Based VTI, AnyConnect / Secure Client) |
| **Cloud & Identity** | Microsoft Azure (VNet, VPN Gateway, NAT Gateway), Microsoft Entra ID (SAML SSO, Conditional Access MFA), Active Directory |
| **Security & NAC** | Cisco ISE (RADIUS, Dynamic VLAN Assignment), PKI / Let's Encrypt Certificates |
| **Automation & Telemetry** | Ansible, Nautobot, Git, PRTG Network Monitor, Grafana, Telegraf, Wireshark |

---

*Note: All IP addressing, domains, and configurations documented in this portfolio reflect the isolated Meridian lab environment.*
