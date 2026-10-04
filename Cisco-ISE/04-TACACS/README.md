# Cisco ISE — TACACS+ Device Administration

## Overview

This section documents the implementation of Terminal Access Controller Access-Control System Plus (TACACS+) for centralized network administrator access within the Meridian Financial Services environment, powered by Cisco Identity Services Engine (ISE).

While RADIUS is used for network endpoint access (802.1X, MAB, Guest), TACACS+ is strictly reserved for **Device Administration**. It provides granular, identity-based control over who can access network infrastructure, what commands they are allowed to execute, and a comprehensive audit trail of their actions.

---

## Architecture & AAA Workflow

TACACS+ separates the AAA (Authentication, Authorization, Accounting) functions into distinct, encrypted TCP (port 49) transactions, allowing for granular policy enforcement.

![ISE](screenshots/tacacs-visio.png)
---

## Design Objectives

- **Centralized Administration:** Eliminate local username/password databases on individual network devices.
- **Granular Command Authorization:** Utilize ISE Shell Profiles and Command Sets to restrict or permit specific CLI commands based on the administrator's role.
- **Privilege Escalation Control:** Automatically assign Privilege Level 15 upon successful authentication for authorized network admins.
- **Non-Repudiation & Auditing:** Leverage TACACS+ Accounting to log every command executed by an administrator, tied to their specific identity, for security compliance and troubleshooting.

---

## Functional Validation Scope

The implementation was rigorously tested across three distinct scenarios to prove the AAA workflow:

1. **Positive Authentication & Authorization:** Validating that a legitimate admin (`netadmin.test`) successfully authenticates, receives Privilege 15, and can execute permitted commands.
2. **Negative Authentication:** Validating that invalid credentials are immediately rejected by ISE, and the device denies access.
3. **Accounting Verification:** Validating that command execution generates accurate Start/Stop accounting records in ISE.

---

## Scope & Boundaries

This directory strictly covers **TACACS+ Device Administration**. 

Related but distinct ISE capabilities are documented in their respective sections:
- **Foundation (AD/RADIUS):** `Cisco-ISE/01-AD-RADIUS/`
- **Corporate Endpoint Access (802.1X):** `Cisco-ISE/02-802.1X/`
- **Guest/Unknown Endpoint Access:** `Cisco-ISE/03-Guest/`

---

## Documentation Structure

| Document | Purpose |
| :--- | :--- |
| `README.md` | Architecture, AAA workflow, and design objectives. |
| `configuration.md` | ISE Shell Profiles, Command Sets, IOS device configuration, and evidence matrix. |
| `screenshots/` | Curated evidence of policy configuration, Live Logs, and CLI validation. |
