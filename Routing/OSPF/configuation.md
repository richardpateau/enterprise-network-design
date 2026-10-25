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

## 1. Steady-State Operational Verification

Before testing failure scenarios, the baseline health of the OSPF domain was verified to ensure correct configuration and adjacency formation.

### 1.1 OSPF Process & Router ID
**Command:** `show ip ospf`  
**Validation Criteria:** Confirms OSPF process 10 is active, the correct static Router ID is assigned, and expected areas are present.  
**Observation:** Router ID is correctly set (e.g., `10.255.10.1`), and the process is actively running with the expected area assignments.

![OSPF](screenshots/hq-edge1-sh-ospf.png)


### 1.2 Neighbor Adjacencies
**Command:** `show ip ospf neighbor`  
**Validation Criteria:** Verifies that expected OSPF adjacencies have formed and reached the `FULL` state.    
**Observation:** All expected peers are visible in the `FULL` state, confirming successful Database Description (DD) packet exchange and LSDB synchronization.

![OSPF](screenshots/hq-edge1-sh-ip-ospf-neighbor.png)

### 1.3 Routing Table & Path Selection
**Command:** `show ip route ospf`  
**Validation Criteria:** Confirms OSPF-learned routes are installed in the Routing Information Base (RIB). Intra-area routes appear as `O`, and inter-area routes as `O IA`.    
**Observation:** Remote Meridian site networks (Areas 20, 30, 40, 50) are successfully learned via `O IA` routes, proving correct Area Border Router (ABR) functionality.

![OSPF](screenshots/hq-edge1-sh-ip-route-ospf.png)

### 1.4 Link-State Database (LSDB)
**Command:** `show ip ospf database`  
**Validation Criteria:** Verifies LSAs are being exchanged and the topology database is synchronized across the area.    

![OSPF](screenshots/hq-edge1-sh-ospf-database.png)

### 1.5 Multi-Area & Passive Interface Validation
**Command:** `show ip ospf interface brief`  
**Validation Criteria:** Confirms site-specific networks are segmented into their correct areas and that endpoint-facing VLAN interfaces are correctly set to `PASSIVE`.    
**Observation:** Passive interfaces successfully advertise their connected subnets into OSPF without attempting to form unnecessary or insecure neighbor adjacencies.

![OSPF](screenshots/hq-edge1-sh-ip-ospf-interface-brief.png)

---

## 2. Functional Failover Testing (Resiliency)

**Objective:** Demonstrate that the Meridian network maintains routing continuity when a primary OSPF path fails, and correctly reconverges upon recovery.

### 2.1 Pre-Failure Baseline
Before inducing a failure, the baseline state was captured to confirm normal routing and connectivity.
- **Neighbor State:** Primary adjacency is `FULL`.
- **Routing Table:** Destination is reachable via the primary next-hop.
- **Connectivity:** Continuous ICMP ping to a remote destination (e.g., Ashburn DR subnet) is successful.  

**OSPF Topology**

![OSPF](screenshots/ospf-topology.png)

**CHI-R1 show ip ospf neighbor**

![OSPF](screenshots/ospf-failover-before-neighbor.png)

**CHI-R1: Routing table**

![OSPF](screenshots/ospf-failover-before-routes.png)

**CHI-R1: PC1 successful ping to HQ-PC2**

![OSPF](screenshots/ospf-failover-before-connectivity.png)

### 2.2 Failure Injection
A controlled failure was introduced by administratively shutting down the primary OSPF transit interface (e.g., `interface FastEthernet0/0` → `shutdown`).

![OSPF](screenshots/CHI-R1-intentional-shutdown.png)

### 2.3 Convergence Observation
Immediately following the failure, the network state was re-evaluated:
- **Neighbor State:** The failed adjacency transitioned to `DOWN`.
- **Routing Table:** OSPF rapidly recalculated the SPF tree, removing the failed path and installing the alternate path into the RIB.  

**Neighbor state during failure**

![OSPF](screenshots/CHI-R1-neighbor-during-failure.png)

**Routing table during failure**

![OSPF](screenshots/CHI-R1-intentional-shutdown.png)

### 2.4 Connectivity Validation
- **Ping Test:** The continuous ping experienced a brief, acceptable interruption (typically 1–3 dropped packets, aligning with OSPF dead timer defaults) before seamlessly restoring connectivity via the alternate path.
- **Traceroute:** Confirmed traffic is now flowing through the redundant topology.  

**Unbroken ping from CHI PC1**

![OSPF](screenshots/pc-continuous-ping.png)

**Traceroute before and after failure**

![OSPF](screenshots/ospf-traceroute.png)

### 2.5 Path Recovery
The failed interface was restored (`no shutdown`). OSPF successfully re-established the adjacency, and the routing table reconverged to the intended primary operational state without disrupting ongoing traffic.  

---

## 3. Protocol Integration Notes

### Firewall HA & OSPF
The Meridian edge utilizes an Active/Standby firewall HA pair. For OSPF verification purposes, this pair is treated as a **single logical routing endpoint**. Verification focuses on the operational adjacency to the HA virtual IP, rather than treating the physical chassis as independent OSPF peers.

![OSPF](screenshots/hw-fw1-sh-ospf-neighbor.png)

### HSRP & OSPF Boundary
HSRP provides local first-hop redundancy (Active/Standby gateways), while OSPF handles dynamic path calculation across the routed WAN. These protocols operate independently but complement each other. HSRP-specific failover testing is documented separately in `Routing/verification/hsrp-verification.md`.

---

## 4. Verification Evidence Matrix

| Verification Area | Command(s) Used | Status | Evidence File |
| :--- | :--- | :---: | :--- |
| OSPF Process & Router ID | `show ip ospf` | ✅ Verified | `ospf-process.png` |
| Neighbor Adjacencies | `show ip ospf neighbor` | ✅ Verified | `ospf-neighbors.png` |
| Route Installation | `show ip route ospf` | ✅ Verified | `ospf-routes.png` |
| LSDB Synchronization | `show ip ospf database` | ✅ Verified | `ospf-database.png` |
| Multi-Area & Passive Interfaces | `show ip ospf interface brief` | ✅ Verified | `ospf-passive-interface.png` |
| Failover Convergence | `show ip route`, `ping` | ✅ Verified | `ospf-failover-*.png` |

*(Note: Status reflects completed lab validation. If a specific test has not yet been executed in your environment, simply change "✅ Verified" to "⏳ Pending".)*

---
