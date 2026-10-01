# EtherChannel - LACP

## Overview

This section documents the implementation and verification of EtherChannel using Link Aggregation Control Protocol (LACP) across the Meridian Financial Services switching environment.

LACP is used to combine multiple physical Ethernet links into a single logical Port-channel interface.

The implementation provides:

- Link aggregation
- Increased logical bandwidth
- Link redundancy
- Simplified Layer 2 topology
- Dynamic negotiation of EtherChannel membership
- Resiliency against the failure of an individual physical member link

All documented EtherChannel bundles use LACP.

---

## Design

The switching environment uses Layer 2 LACP EtherChannels between redundant switch pairs.

### HQ

![Etherchannel](screenshots/lacp.png)

Both HQ switch pairs use two physical interfaces as members of Port-channel1.

### Branch Offices

Chicago, Dallas, and Miami each use two physical interfaces between their switch pairs.

![Etherchannel](screenshots/branch-lacp.png)

### Ashburn

Ashburn uses Ethernet0/2 and Ethernet0/3 between ASH-SW-3 and ASH-SW-4.

![Etherchannel](screenshots/ashburn-lacp.png)

### EtherChannel Inventory

| Site | Switch Pair | Port-channel | Member Interfaces | Protocol |
|---|---|---|---|---|
| HQ | HQ-SW-1 ↔ HQ-SW-2 | Po1 | E0/1, E0/2 | LACP |
| HQ | HQ-SW-3 ↔ HQ-SW-4 | Po1 | E0/1, E0/2 | LACP |
| Chicago | CHI-SW-1 ↔ CHI-SW-2 | Po1 | E0/1, E0/2 | LACP |
| Dallas | DAL-SW-1 ↔ DAL-SW-2 | Po1 | E0/1, E0/2 | LACP |
| Miami | MIA-SW-1 ↔ MIA-SW-2 | Po1 | E0/1, E0/2 | LACP |
| Ashburn | ASH-SW-3 ↔ ASH-SW-4 | Po1 | E0/2, E0/3 | LACP |

---

## Operational Verification

EtherChannel operation was verified using:

```text
show etherchannel summary
show interfaces port-channel 1
show lacp neighbor
```

The verification confirmed that the documented Port-channel interfaces are operational and that the physical member interfaces are bundled into their respective LACP groups.

A successful EtherChannel appears in `show etherchannel summary` with:

```text
Po1(SU)   LACP
Et0/x(P)  Et0/x(P)
```

Where:

- S = Layer 2 EtherChannel
- U = Port-channel is in use
- LACP = LACP is the negotiation protocol
- P = Physical interface is bundled into the Port-channel

---

## Verification Results

### HQ

#### HQ-SW-1 ↔ HQ-SW-2

Verified:

```text
Group  Port-channel  Protocol
1      Po1(SU)        LACP

Et0/1(P)
Et0/2(P)
```

![Etherchannel](screenshots/hq-sw1-etherchannel-summary.png)

Port-channel1 was verified as:

```text
Port-channel1 is up, line protocol is up
```
![Etherchannel](screenshots/hq-sw1-port-channel1.png)

LACP neighbor information identified HQ-SW-2 as the partner.

![Etherchannel](screenshots/hq-sw1-lacp-neighbor.png)

#### HQ-SW-3 ↔ HQ-SW-4

Verified:

```text
Group  Port-channel  Protocol
1      Po1(SU)        LACP

Et0/1(P)
Et0/2(P)
```

Port-channel1 was verified as:

```text
Port-channel1 is up, line protocol is up
```

LACP neighbor information identified HQ-SW-4 as the partner.

### Chicago

#### CHI-SW-1 ↔ CHI-SW-2

CHI-SW-1 verified:

```text
Po1(SU)   LACP
Et0/1(P)
Et0/2(P)
```

Port-channel1 was verified as up/up.

LACP neighbor information identified CHI-SW-2 as the partner.

CHI-SW-2 independently verified:

```text
Po1(SU)   LACP
Et0/1(P)
Et0/2(P)
```

Port-channel1 was also verified as up/up.

### Dallas

#### DAL-SW-1 ↔ DAL-SW-2

DAL-SW-1 verified:

```text
Po1(SU)   LACP
Et0/1(P)
Et0/2(P)
```

Port-channel1 was verified as up/up.

LACP neighbor information identified DAL-SW-2 as the partner.

DAL-SW-2 independently verified:

```text
Po1(SU)   LACP
Et0/1(P)
Et0/2(P)
```

Port-channel1 was also verified as up/up.

### Miami

#### MIA-SW-1 ↔ MIA-SW-2

MIA-SW-1 verified:

```text
Po1(SU)   LACP
Et0/1(P)
Et0/2(P)
```

Port-channel1 was verified as up/up.

LACP neighbor information identified MIA-SW-2 as the partner.

MIA-SW-2 independently verified:

```text
Po1(SU)   LACP
Et0/1(P)
Et0/2(P)
```

Port-channel1 was also verified as up/up.

### Ashburn

#### ASH-SW-3 ↔ ASH-SW-4

ASH-SW-3 verified:

```text
Po1(SU)   LACP
Et0/2(P)
Et0/3(P)
```

Port-channel1 was verified as up/up.

LACP neighbor information identified ASH-SW-4 as the partner.

ASH-SW-4 independently verified:

```text
Po1(SU)   LACP
Et0/2(P)
Et0/3(P)
```

Port-channel1 was also verified as up/up.

---

## Verification Summary

All documented LACP bundles were operational during testing.

| Site | Port-channel | Member Links | Operational |
|---|---|---|---|
| HQ | HQ-SW-1 Po1 | E0/1, E0/2 | Yes |
| HQ | HQ-SW-3 Po1 | E0/1, E0/2 | Yes |
| Chicago | CHI-SW-1 Po1 | E0/1, E0/2 | Yes |
| Chicago | CHI-SW-2 Po1 | E0/1, E0/2 | Yes |
| Dallas | DAL-SW-1 Po1 | E0/1, E0/2 | Yes |
| Dallas | DAL-SW-2 Po1 | E0/1, E0/2 | Yes |
| Miami | MIA-SW-1 Po1 | E0/1, E0/2 | Yes |
| Miami | MIA-SW-2 Po1 | E0/1, E0/2 | Yes |
| Ashburn | ASH-SW-3 Po1 | E0/2, E0/3 | Yes |
| Ashburn | ASH-SW-4 Po1 | E0/2, E0/3 | Yes |

---

## Evidence

Screenshots for this section are stored in:

```text
Switching/EtherChannel-LACP/screenshots/
```

The evidence set includes representative verification from HQ, Chicago, Dallas, Miami, and Ashburn.

Recommended evidence:

```text
hq-sw1-etherchannel-summary.png
hq-sw1-lacp-neighbor.png
hq-sw1-port-channel1.png
chi-sw1-etherchannel-summary.png
dal-sw1-etherchannel-summary.png
mia-sw1-etherchannel-summary.png
ash-sw3-etherchannel-summary.png
```

The complete verification was performed on both sides of each documented EtherChannel. The screenshot set is intentionally representative rather than duplicating identical output from every switch.

---

## Verification Commands

```text
show etherchannel summary
show interfaces port-channel 1
show lacp neighbor
```

These commands verify:

- EtherChannel membership
- LACP negotiation
- Port-channel state
- Physical member state
- LACP neighbor relationships
- Logical Port-channel operation

---

## Result

The documented Meridian switching environment successfully established and verified Layer 2 EtherChannels using LACP across the HQ, branch, and Ashburn switching environments.
