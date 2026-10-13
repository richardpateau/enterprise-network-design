### `Switching/Port-Security/README.md`

# Port Security — Access Layer Endpoint Protection

## Overview

This section documents the implementation of Cisco switchport security within the Meridian Financial Services switching environment. Port Security is deployed on endpoint-facing access ports to control which MAC addresses are permitted to utilize a switchport, preventing unauthorized Layer 2 access.

## Design Objectives

- **MAC Address Limiting:** Restrict the number of permitted MAC addresses per endpoint port.
- **Dynamic Learning:** Utilize sticky MAC learning to dynamically bind legitimate endpoint hardware addresses.
- **Violation Enforcement:** Apply distinct violation responses (Restrict vs. Shutdown) based on endpoint use cases.
- **Defense in Depth:** Integrate Port Security with 802.1X, PortFast, and BPDU Guard on access ports.

## Port Security Profiles

The documented implementation on HQ-SW-2 utilizes two distinct security profiles tailored to specific endpoint types:

| Switch | Interface | Endpoint Use Case | Max MACs | Learning Method | Violation Mode |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **HQ-SW-2** | `Ethernet1/0` | PC1 (Standard User) | 2 | Sticky | **Restrict** |
| **HQ-SW-2** | `Ethernet1/2` | Printer / MAB Test | 1 | None (Static) | **Shutdown** |

### Profile 1: Standard User (Restrict Mode)
Applied to `Ethernet1/0`. Allows up to two MAC addresses (accommodating the PC and potentially a softphone/VM). Uses **sticky learning** to automatically bind the MAC addresses. The **restrict** violation mode drops unauthorized traffic and increments the violation counter/syslog without taking the port down, ensuring user productivity is not interrupted by transient MAC changes.

![Port-Security](screenshots/hq-sw2-e1-0-port-security-status.png)

### Profile 2: IoT/Printer (Shutdown Mode)
Applied to `Ethernet1/2`. Hard-limited to a single MAC address. Uses the **shutdown** violation mode. If an unauthorized device is connected, the port is immediately placed into an `err-disabled` state, providing strict isolation for static IoT devices.

![Port-Security](screenshots/hq-sw2-e1-2-port-security-status.png)

## Integrated Access Security

Port Security is not deployed in isolation. Both documented interfaces integrate with broader access-layer security features:

- **802.1X Authentication:** `authentication port-control auto` and `dot1x pae authenticator` are enabled.
- **Spanning-Tree Optimization:** `spanning-tree portfast` is enabled to bypass listening/learning states.
- **Loop Prevention:** `spanning-tree bpduguard enable` is applied to `Ethernet1/0` to immediately disable the port if a rogue switch is connected.

![Port-Security](screenshots/hq-sw2-e1-0-port-security-config.png)

## Current Operational State

Verification of the HQ-SW-2 Port Security summary confirms the design is active and stable:

```text
Secure Port  MaxSecureAddr  CurrentAddr  SecurityViolation  Security Action
      Et1/0              2            2                  0         Restrict
      Et1/2              1            0                  0         Shutdown
```

- **Et1/0:** Has successfully learned and bound its two permitted sticky MAC addresses. Zero violations.
- **Et1/2:** Awaiting its first learned MAC address. Zero violations.

![Port-Security](screenshots/hq-sw2-port-security-summary.png)

## Evidence & Verification

Configuration and state verification screenshots are stored in:
`Switching/Port-Security/screenshots/`

**Recommended Evidence Set:**
- `hq-sw2-e1-0-port-security-config.png`
- `hq-sw2-e1-0-port-security-status.png`
- `hq-sw2-e1-2-port-security-config.png`
- `hq-sw2-e1-2-port-security-status.png`
- `hq-sw2-port-security-address-table.png`

*Note: Detailed security-violation testing (rogue device packet loss, syslog generation, err-disabled state recovery) is documented separately in the project's verification structure to maintain a clean separation between design implementation and test execution.*
