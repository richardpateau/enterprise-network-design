# Layer 2 Switching Architecture

## Overview

This directory documents the Layer 2 switching design, implementation, and operational validation for the Meridian Financial Services enterprise network. 

The switching infrastructure is distributed across the Headquarters (HQ), multiple branch offices (Chicago, Dallas, Miami), and the Ashburn Disaster Recovery (DR) site. The design provides a structured, resilient, and secure foundation through:

- Strict VLAN segmentation
- Predictable Spanning Tree Protocol (STP) topology
- Link redundancy and aggregation via LACP EtherChannel
- Defense-in-depth access-port security (802.1X, MAB, Port Security, BPDU Guard)
- Comprehensive operational verification and functional failure testing

---

## Switching Architecture

The Meridian switching environment utilizes segmented VLANs, redundant uplinks, and standardized access policies to ensure high availability and strict traffic isolation.

### Standard Enterprise VLANs

| VLAN | Name | Purpose |
| :---: | :--- | :--- |
| **10** | `USERS` | Standard user endpoints |
| **20** | `VOICE` | VoIP endpoints |
| **30** | `SERVERS` | Server infrastructure |
| **40** | `GUEST` | Isolated guest access |
| **50** | `MANAGEMENT` | Out-of-band network management |
| **60** | `PRINTERS_IOT` | Printers and static IoT devices |
| **70** | `NETWORK_INFRA` | Network infrastructure links |
| **999** | `NATIVE_UNUSED` | Unused / secure native VLAN |

*Note: The Ashburn DR site utilizes additional site-specific VLANs (110–150) for localized access networks, as detailed in the Ashburn site design documentation.*

---

## Switching Features

### VLANs
VLANs provide strict Layer 2 segmentation between different classes of Meridian devices and users.
- **Implementation:** Access VLAN assignment, 802.1Q trunking, explicit allowed-VLAN lists, and dedicated management/native VLANs.
- **Documentation:** [`VLAN/`](VLAN/)

### Spanning Tree Protocol (STP)
STP provides Layer 2 loop prevention and determines optimal forwarding paths within the switching topology.
- **Implementation:** Centralized root bridge selection (HQ-SW-1), optimized root/designated port roles, and rapid edge-port convergence.
- **Documentation:** [`STP/`](STP/)

### LACP EtherChannel
Link Aggregation Control Protocol (LACP) combines multiple physical links into logical Port-Channels.
- **Implementation:** Provides link aggregation, increased logical bandwidth, and seamless N+1 redundancy. Survives individual member-link failures without dropping active sessions.
- **Documentation:** [`Etherchannel/`](Etherchannel/)

### Port Security
Port Security provides an additional Layer 2 access-control mechanism on endpoint-facing ports.
- **Implementation:** Maximum secure MAC address limits, sticky MAC learning, and tailored violation modes (`restrict` for users, `shutdown` for IoT).
- **Documentation:** [`Port-Security/`](Port-Security/)

### BPDU Guard
BPDU Guard protects endpoint-facing PortFast interfaces from unexpected Spanning Tree BPDUs.
- **Implementation:** Automatically places protected access ports into an `err-disabled` state upon detecting rogue switches, preventing accidental or malicious Layer 2 loops.
- **Documentation:** [`BPDU-Guard/`](BPDU-Guard/)

---

## Access-Port Security Model

Meridian employs a defense-in-depth strategy, layering multiple controls on endpoint-facing ports rather than relying on a single feature. 

```text
Endpoint Device
       │
       ▼
Access Switch Port
  ├── 802.1X / MAB      (Identity-based Network Access Control)
  ├── Port Security     (MAC Address Limiting & Sticky Learning)
  ├── PortFast          (Rapid Transition to Forwarding State)
  └── BPDU Guard        (Strict Loop Prevention Boundary)
       │
       ▼
Assigned VLAN
```

### Infrastructure vs. Endpoint Separation
- **Endpoint Ports:** May utilize 802.1X, MAB, Port Security, PortFast, and BPDU Guard.
- **Infrastructure Links:** Switch-to-switch and router-to-switch uplinks utilize 802.1Q trunking and LACP. Endpoint-specific protections (like PortFast and BPDU Guard) are **explicitly excluded** from these links to preserve legitimate STP topology.
- **Unused Ports:** Administratively shut down and assigned to the secure, unused native VLAN (999) to minimize the attack surface.

---

## Verification & Testing Strategy

Operational verification and functional testing are maintained separately from configuration documentation to ensure a clean separation of concerns. All testing evidence is centralized in the [`verification/`](verification/) directory.

### Verification Scope
- **VLANs:** Membership, trunk negotiation, and strict inter-VLAN isolation.
- **STP:** Root bridge election, port roles, and rapid reconvergence during link failures.
- **LACP:** Bundle state, neighbor adjacency, and zero-packet-loss member link failover.
- **Port Security:** Secure MAC binding, violation detection, and restrict/shutdown enforcement.
- **BPDU Guard:** Edge-port protection and automatic `err-disabled` response to rogue BPDUs.

---

## Directory Structure

```text
Switching/
│
├── README.md                          # This file
│
├── VLAN/                              # VLAN design & config
├── STP/                               # STP design & config
├── Etherchannel/                      # LACP design & config
├── Port-Security/                     # Port Security design & config
├── BPDU-Guard/                        # BPDU Guard design & config
│
├── configs/                           # Raw switch configuration files
│   ├── hq-sw1.txt
│   ├── hq-sw2.txt
│   ├── chi-sw1.txt
│   ├── dal-sw1.txt
│   ├── mia-sw1.txt
│   └── ash-sw1.txt
│   └── ...
│
└── verification/                      # Operational & functional testing
    ├── README.md                      # Verification testing
    ├── vlan-verification.md
    ├── stp-verification.md
    ├── lacp-verification.md
    ├── port-security-verification.md
    ├── bpdu-guard-verification.md
    └── screenshots/
```

---

## Design Principles

This implementation is guided by core enterprise networking principles:

1. **Strict Segmentation:** Isolate users, voice, servers, guests, management, and infrastructure traffic into dedicated broadcast domains.
2. **Predictable Redundancy:** Utilize redundant physical paths and LACP to eliminate single points of failure at the access and distribution layers.
3. **Proactive Loop Prevention:** Enforce STP boundaries rigorously; never trust an endpoint port to behave predictably.
4. **Role-Based Security:** Apply 802.1X, MAB, Port Security, and BPDU Guard dynamically based on the specific role of the port (User vs. IoT vs. Infrastructure).
5. **Operational Validation:** No configuration is considered complete without both steady-state operational verification and controlled functional failure testing.

---

## Related Documentation

- **Enterprise Standards:** [`docs/standards/`](../docs/standards/)
- **Switch Configurations:** [`Switching/configs/`](configs/)
- **Switching Verification:** [`Switching/verification/`](verification/)
- **Project-Level Test Evidence:** Root-level `VLAN Config test/`, `STP/`, `LACP Testing/`, `Port Security Test/`, and `BPDU Guard/` directories.
