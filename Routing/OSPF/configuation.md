# OSPF Configuration Model

## Overview

Meridian Financial Services utilizes a unified OSPF Process `10` across the entire enterprise routing domain. This document outlines the standard configuration models for the Area 0 backbone and the site-specific non-backbone areas.

All routers use explicitly configured Router IDs to ensure process stability.

---

## 1. Area 0 Backbone Configuration (HQ)

The HQ infrastructure forms the OSPF backbone. Routers in this area advertise loopback interfaces, routed infrastructure networks, and WAN transit links.

### HQ-R1 (Core Router)
```cisco
router ospf 10
 router-id 10.255.10.11
 !
 ! --- Loopback & Infrastructure ---
 network 10.255.10.11 0.0.0.0 area 0
 network 10.255.112.0 0.0.0.7 area 0
 !
 ! --- WAN Transit Link ---
 network 172.16.0.12 0.0.0.3 area 0
```

### HQ-R2, HQ-EDGE-1, HQ-EDGE-2
These devices follow the exact same Area 0 configuration model, utilizing their respective statically assigned Router IDs:
* **HQ-R2:** `router-id 10.255.10.12`
* **HQ-EDGE-1:** `router-id 10.255.10.1`
* **HQ-EDGE-2:** `router-id 10.255.10.2`

---

## 2. Branch Area Configuration Model (ABRs)

Branch routers act as Area Border Routers (ABRs). They maintain an Area 0 adjacency over their WAN transit links while advertising their local site VLANs into their designated non-backbone area.

### Representative ABR Configuration (Chicago - Area 20)
```cisco
router ospf 10
 router-id 10.255.20.1
 !
 ! --- Passive Interface Enforcement ---
 passive-interface default
 !
 ! Explicitly allow OSPF adjacency ONLY on trusted transit links
 no passive-interface GigabitEthernet0/0   ! Example: WAN link to HQ (Area 0)
 no passive-interface GigabitEthernet0/1   ! Example: LAN transit to CHI-R2 (Area 20)
 !
 ! --- Area 0: WAN Transit to Backbone ---
 network 172.16.20.0 0.0.0.3 area 0
 !
 ! --- Area 20: Local Site VLANs ---
 network 10.20.10.0 0.0.0.255 area 20
 network 10.20.20.0 0.0.0.255 area 20
 network 10.20.30.0 0.0.0.255 area 20
 network 10.20.40.0 0.0.0.255 area 20
 network 10.20.50.0 0.0.0.255 area 20
 network 10.20.60.0 0.0.0.255 area 20
 network 10.20.70.0 0.0.0.255 area 20
```

### Site-Specific Area Assignments
The exact subnet assignments follow the standardized Meridian IP addressing scheme per site:

| Site | OSPF Area | Router IDs | Advertised VLAN Subnets (Area X) |
| :--- | :---: | :--- | :--- |
| **Chicago** | **20** | `10.255.20.1` / `.2` | `10.20.10.0/24` through `10.20.70.0/24` |
| **Dallas** | **30** | `10.255.30.1` / `.2` | `10.30.10.0/24` through `10.30.70.0/24` |
| **Miami** | **40** | `10.255.40.1` / `.2` | `10.40.10.0/24` through `10.40.70.0/24` |

---

## 3. Ashburn DR Site Configuration (Area 50)

The Ashburn site utilizes Router-on-a-Stick (ROAS) subinterfaces for its internal VLAN routing. The OSPF configuration specifically targets these subinterfaces and enforces strict passive-interface policies.

### Ashburn Internal Router
```cisco
router ospf 10
 router-id 10.255.50.1
 !
 ! --- Area 50: Local Site VLAN Subinterfaces ---
 network 10.50.10.0 0.0.0.255 area 50
 network 10.50.20.0 0.0.0.255 area 50
 network 10.50.30.0 0.0.0.255 area 50
 network 10.50.40.0 0.0.0.255 area 50
 network 10.50.50.0 0.0.0.255 area 50
 !
 ! --- Passive Interface Enforcement ---
 ! Prevents OSPF hello packets on endpoint-facing SVIs
 passive-interface FastEthernet0/0.110
 passive-interface FastEthernet0/0.120
 passive-interface FastEthernet0/0.130
 passive-interface FastEthernet0/0.140
 passive-interface FastEthernet0/0.150
```
*Note: Ashburn Edge routers (`ASH-R1/R2`) follow the standard ABR model, connecting Area 50 to the Area 0 backbone via WAN transit links.*

---

## 4. Configuration Best Practices Applied

1. **Explicit Router IDs:** Every router uses `router-id x.x.x.x` under the OSPF process to prevent unpredictable elections based on interface IP addresses.
2. **Precise Wildcard Masks:** Network statements use exact wildcard masks (e.g., `0.0.0.0` for host routes, `0.0.0.3` for /30 WAN links, `0.0.0.255` for /24 VLANs) to ensure only intended interfaces participate in OSPF.
3. **Passive Interface Enforcement:** Endpoint-facing VLAN interfaces and Loopbacks are explicitly configured as `passive-interface`. This advertises the connected subnet into the OSPF domain without attempting to form unnecessary or insecure neighbor adjacencies.

---

## Verification

Operational verification, including neighbor adjacency states, Router ID validation, LSDB integrity, and convergence behavior during intentional link failures, is documented separately.

See: [`Routing/verification/ospf-verification.md`](../verification/ospf-verification.md)
