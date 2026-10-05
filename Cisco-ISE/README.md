Here is the polished, portfolio-ready version of your top-level `Cisco-ISE/README.md`. 

I have elevated the language to match the senior enterprise-engineer tone of the rest of your portfolio, removed the AI artifacts (like the chatgpt references), and made the **"No MAB"** scope boundary highly visible and professional. This ensures the document reads as a deliberate architectural choice rather than a missing feature.

***

# Cisco Identity Services Engine (ISE) Implementation

## Overview

This section documents the Cisco Identity Services Engine (ISE) implementation for the Meridian Financial Services enterprise network. 

Cisco ISE serves as the centralized policy and authentication platform for the environment, providing identity-driven network access control (NAC) and secure network-device administration. By integrating with Microsoft Active Directory, ISE eliminates local credential management on network devices and enforces granular, role-based access policies across the enterprise.

---

## ISE Architecture

![ISE](screenshots/ise-readme-visio.png)

---

## Implemented ISE Functions

The Meridian ISE implementation is modularized into four primary functional areas. Each area maintains its own dedicated documentation, configuration model, and evidence repository.

### 01 — Active Directory & RADIUS Integration
Establishes the foundational trust between Cisco ISE and the enterprise directory.
- **Key Implementations:** Active Directory domain join, AD group mapping, RADIUS network device definitions, and centralized identity-source sequencing.
- **Documentation:** [`01-AD-RADIUS/`](./01-AD-RADIUS/)

### 02 — 802.1X Network Access Control (NAC)
Provides port-based, identity-driven access control for corporate endpoints.
- **Key Implementations:** 802.1X authentication policies, dynamic VLAN assignment (VLAN 10) based on AD group membership, and rigorous positive/negative testing (including rogue endpoint blocking).
- **Documentation:** [`02-802.1X/`](./02-802.1X/)

### 03 — Guest & Unknown Device Access
Delivers controlled, segmented network access for unmanaged or temporary endpoints.
- **Key Implementations:** Unknown-device policy conditions, Guest authorization profiles, and dynamic assignment to a restricted guest network (VLAN 40) with DHCP provisioning.
- **Scope Boundary:** *This implementation intentionally excludes MAC Authentication Bypass (MAB).* Guest access is strictly governed by the documented unknown-device RADIUS workflow to maintain a clear, auditable security boundary.
- **Documentation:** [`03-Guest/`](./03-Guest/)

### 04 — TACACS+ Network Administration
Secures administrative access to network infrastructure through centralized AAA.
- **Key Implementations:** TACACS+ authentication, role-based shell profiles (Privilege 15), granular command-set authorization, and comprehensive TACACS+ command accounting for non-repudiation.
- **Documentation:** [`04-TACACS/`](./04-TACACS/)

---

## Authentication & Authorization Model

The Meridian design strictly separates endpoint network access from infrastructure device administration, ensuring the Principle of Least Privilege (PoLP).

| Use Case | Protocol | Identity / Policy Source | Authorization Result |
| :--- | :--- | :--- | :--- |
| **Corporate Endpoint Access** | RADIUS (802.1X) | AD Group Membership | Dynamic VLAN 10 Assignment |
| **Guest / Unknown Access** | RADIUS | Unknown Device Condition | Restricted VLAN 40 Assignment |
| **Network Device Administration** | TACACS+ | Network Admin AD Group | Privilege 15 + Command Sets |

---

## Testing & Validation Strategy

The ISE implementation was rigorously validated using both positive and negative test cases to prove policy enforcement, not just configuration.

### ✅ Positive Validation
- Successful AD integration and user resolution.
- Successful 802.1X authentication and dynamic VLAN 10 assignment.
- Successful Guest unknown-device detection and VLAN 40 assignment.
- Successful Network Administrator SSH login with Privilege 15 and command accounting.

### ❌ Negative Validation
- Invalid 802.1X credentials (Access-Reject).
- Rogue/unauthorized endpoint connection attempts (Blocked).
- Invalid TACACS+ administrative login attempts (Access-Denied with router-side debug verification).

---

## Enterprise Security Posture

This ISE deployment demonstrates several critical enterprise security controls:
1. **Centralized Identity Management:** Eliminates local device accounts; all access ties back to Active Directory.
2. **Dynamic Segmentation:** Endpoints are placed into appropriate VLANs based on identity, not physical port.
3. **Guest Isolation:** Unknown devices are automatically funneled into a restricted, monitored guest network.
4. **Administrative Non-Repudiation:** TACACS+ command accounting ensures every administrative action is logged and tied to a specific user identity.
5. **Comprehensive Visibility:** All authentication successes and failures are captured in ISE Live Logs for security monitoring.

---

## Repository Structure

```text
Cisco-ISE/
├── README.md
├── 01-AD-RADIUS/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
├── 02-802.1X/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
├── 03-Guest/
│   ├── README.md
│   ├── configuration.md
│   └── screenshots/
└── 04-TACACS/
    ├── README.md
    ├── configuration.md
    └── screenshots/
```
---

## Implementation Result

The Meridian ISE implementation successfully delivers a centralized, identity-driven security architecture. By integrating Active Directory, enforcing 802.1X NAC, segmenting guest traffic, and securing device administration via TACACS+, the environment meets enterprise standards for network access control, compliance, and operational visibility.
