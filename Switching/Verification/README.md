# Switching Layer Verification & Testing

## Overview

This directory contains the operational validation and functional testing evidence for the Meridian Financial Services Layer 2 switching infrastructure. 

While the `../Switching/` feature directories document the *design and configuration*, this directory proves that the implementation behaves as expected under both normal operating conditions and simulated failure scenarios.

---

## Verification Philosophy

Validation is executed using a two-tiered approach to ensure both baseline stability and resiliency:

1. **Operational Verification (Steady State)**  
   Confirms the feature is currently functioning as designed in a healthy network.  
   *Method:* Cisco IOS `show` commands, neighbor adjacencies, and interface state validation.

2. **Functional Failure Testing (Resiliency)**  
   Intentionally exercises the network to confirm expected failover or protective behavior.  
   *Method:* Controlled interface shutdowns, rogue device injection, and continuous ping/traceroute monitoring to validate zero or minimal packet loss.

---

## Verification Matrix

| Feature | Operational Validation | Functional Failure Test |
| :--- | :--- | :--- |
| **VLANs** | Trunk negotiation, access-port assignments, VLAN database consistency. | Inter-VLAN routing isolation; verifying VLAN 10 cannot ping VLAN 20 without a router. |
| **STP** | Root bridge election, port roles (Designated/Alternate), PortFast status. | Intentional root port failure; verifying rapid reconvergence and backup port promotion. |
| **LACP** | Port-channel `SU` state, LACP neighbor adjacency, member port bundling `(P)`. | Active member link shutdown; verifying continuous ping with 0% packet loss. |
| **Port Security** | Secure MAC table population, sticky learning, violation counters. | Rogue MAC injection; verifying `restrict` drops traffic or `shutdown` triggers `err-disabled`. |
| **BPDU Guard** | PortFast enabled, BPDU Guard active, 0 BPDUs received on edge ports. | Rogue switch connection; verifying immediate transition to `err-disabled` state. |

---

## Evidence Structure

Feature-specific verification screenshots and test artifacts are organized logically to show the **Before**, **During**, and **After** states of each test.

```text
Switching/Verification/
├── README.md                     # This file
├── VLAN/                         # VLAN isolation and trunking tests
├── STP/                          # Root bridge and failover tests
├── EtherChannel-LACP/            # Link aggregation and member failover tests
├── Port-Security/                # MAC violation and restrict/shutdown tests
└── BPDU-Guard/                   # Rogue switch err-disabled tests
```
---

## Related Documentation

For design rationale, configuration models, and steady-state architecture, refer to the implementation directories:

- [VLAN Implementation](../VLAN/)
- [STP Implementation](../STP/)
- [EtherChannel Implementation](../EtherChannel-LACP/)
- [Port Security Implementation](../Port-Security/)
- [BPDU Guard Implementation](../BPDU-Guard/)
