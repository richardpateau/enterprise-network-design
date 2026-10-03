# HSRP Configuration Model

## Overview

Meridian Financial Services utilizes Hot Standby Router Protocol (HSRP) on routed subinterfaces to provide First-Hop Redundancy Protocol (FHRP) for all enterprise VLANs. 

The configuration follows a strict, standardized addressing and templating model to ensure operational consistency across the Headquarters, Branch, and Ashburn DR sites.

---

## 1. Standardized Configuration Model

The HSRP configuration is applied uniformly across all sites. The preferred (Active) router is assigned a higher priority and preemption, while the secondary (Standby) router relies on the default priority (100).

### Active Router Template (Preferred)
```cisco
interface FastEthernet0/0.10
 encapsulation dot1Q 10
 description USERS-VLAN-HSRP-ACTIVE
 ip address 10.10.10.2 255.255.255.0
 !
 ! --- HSRP Configuration ---
 standby version 2
 standby 10 ip 10.10.10.1
 standby 10 priority 110
 standby 10 preempt
```

### Standby Router Template (Secondary)
```cisco
interface FastEthernet0/0.10
 encapsulation dot1Q 10
 description USERS-VLAN-HSRP-STANDBY
 ip address 10.10.10.3 255.255.255.0
 !
 ! --- HSRP Configuration ---
 standby version 2
 standby 10 ip 10.10.10.1
 standby 10 preempt
 ! Priority defaults to 100
```

---

## 2. Site-Specific Implementation Details

While the configuration logic remains identical, the physical interfaces and IP subnets vary by site. The following tables define the exact implementation parameters for each location.

### Headquarters (HQ)
**Interfaces:** `FastEthernet0/0.x`
**Active Router:** HQ-R1 | **Standby Router:** HQ-R2

| VLAN | Subnet | HQ-R1 (Active) | HQ-R2 (Standby) | Virtual Gateway (VIP) | HSRP Group |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 10 | `10.10.10.0/24` | `10.10.10.2` | `10.10.10.3` | `10.10.10.1` | 10 |
| 20 | `10.10.20.0/24` | `10.10.20.2` | `10.10.20.3` | `10.10.20.1` | 20 |
| ... | *(VLANs 30-70 follow identical pattern)* | ... | ... | ... | ... |

### Standard Branches (Chicago, Dallas, Miami)
**Interfaces:** `FastEthernet1/0.x`
**Active Router:** Router 1 (e.g., CHI-R1) | **Standby Router:** Router 2 (e.g., CHI-R2)

| Site | VLAN Range | Router 1 (Active) | Router 2 (Standby) | Virtual Gateway (VIP) |
| :--- | :---: | :--- | :--- | :--- |
| **Chicago** | 10 – 70 | `10.20.x.2` | `10.20.x.3` | `10.20.x.1` |
| **Dallas** | 10 – 70 | `10.30.x.2` | `10.30.x.3` | `10.30.x.1` |
| **Miami** | 10 – 70 | `10.40.x.2` | `10.40.x.3` | `10.40.x.1` |

*(Where `x` represents the specific VLAN identifier, e.g., VLAN 20 uses `10.20.20.2`)*

### Ashburn DR Site
**Interfaces:** `FastEthernet0/0.x`
**Active Router:** ASH-INTERNAL-1 | **Standby Router:** INTERNAL-2
**Note:** Ashburn subinterfaces also integrate OSPF Area 50 directly on the interface.

**Example Configuration (VLAN 110):**
```cisco
! ASH-INTERNAL-1 (Active)
interface FastEthernet0/0.110
 encapsulation dot1Q 110
 ip address 10.50.10.2 255.255.255.0
 standby 110 ip 10.50.10.1
 standby 110 priority 110
 standby 110 preempt
 ip ospf 10 area 50
```

| VLAN | ASH-INTERNAL-1 (Active) | INTERNAL-2 (Standby) | Virtual Gateway (VIP) |
| :---: | :--- | :--- | :--- |
| 110 | `10.50.10.2` | `10.50.10.3` | `10.50.10.1` |
| 120 | `10.50.20.2` | `10.50.20.3` | `10.50.20.1` |
| 130 | `10.50.30.2` | `10.50.30.3` | `10.50.30.1` |
| 140 | `10.50.40.2` | `10.50.40.3` | `10.50.40.1` |
| 150 | `10.50.50.2` | `10.50.50.3` | `10.50.50.1` |

---

## 3. Design Parameters

### HSRP Group Mapping
HSRP group numbers are mapped 1:1 with their corresponding VLAN IDs (e.g., VLAN 10 → Group 10, VLAN 110 → Group 110). This provides a consistent, predictable relationship that simplifies configuration auditing and troubleshooting.

### Priority and Preemption
- **Preferred Router:** Configured with `standby <group> priority 110` and `standby <group> preempt`. This ensures it actively claims the VIP upon boot or recovery.
- **Secondary Router:** Relies on the default HSRP priority of `100`. 

### Virtual Gateway
Endpoints are configured with the HSRP Virtual IP (VIP) as their default gateway. The physical IP addresses of the routers are strictly used for routing protocol adjacencies and management; they are never assigned to endpoints.

---

## 4. Protocol Integration: HSRP vs. OSPF

HSRP and OSPF operate at different layers of the forwarding path but are tightly integrated on the routed subinterfaces (as seen in the Ashburn configuration).

| Feature | HSRP (First-Hop Redundancy) | OSPF (Dynamic Routing) |
| :--- | :--- | :--- |
| **Primary Function** | Provides default-gateway redundancy for endpoints within a specific broadcast domain. | Provides dynamic, loop-free path selection *between* routed network segments. |
| **Operational Scope** | Local to the Layer 2 segment (VLAN). | Enterprise-wide (across Area 0 and non-backbone areas). |
| **Mechanism** | Hello messages between HSRP peers to elect Active/Standby roles for a Virtual IP. | Link-State Advertisements (LSAs) to build a synchronized topology database (LSDB). |

**Integration:** HSRP ensures endpoints always have a valid next-hop. Once traffic reaches the Active HSRP router, OSPF takes over to route that traffic across the WAN to its final destination.

---

## 5. Verification

Operational verification, including `show standby brief` outputs, preemption behavior, and intentional failover testing, is documented separately.

**Expected Verification Commands:**
- `show standby brief`
- `show standby interface FastEthernet0/0.10`
- `show ip interface brief`

See: [`Routing/verification/hsrp-verification.md`](../verification/hsrp-verification.md)
