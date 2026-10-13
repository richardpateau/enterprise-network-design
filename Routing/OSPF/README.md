# OSPF Routing Architecture

## Overview

Meridian Financial Services utilizes Open Shortest Path First (OSPFv2) as the primary Interior Gateway Protocol (IGP) for internal IPv4 routing. 

The OSPF design provides a scalable, hierarchical routing foundation that ensures:
- Dynamic, loop-free routing between all Meridian sites.
- A dedicated, stable Area 0 backbone.
- Site-specific non-backbone areas to limit LSA flooding and optimize SPF calculations.
- Fast convergence following link or device failures.
- Seamless integration with the Firewall High-Availability (HA) and HSRP architectures.

*Note: OSPF is strictly reserved for internal enterprise routing. External routing and hybrid/cloud connectivity are handled separately via BGP.*

---

## Hierarchical OSPF Design

Meridian employs a multi-area OSPF topology to enhance scalability and fault isolation. Area Border Routers (ABRs) connect site-specific areas to the central backbone.

| Location / Function | OSPF Area | Role in Topology |
| :--- | :---: | :--- |
| **HQ / Core** | **Area 0** | OSPF Backbone; interconnects all site areas. |
| **Chicago** | **Area 20** | Branch area; internal VLAN networks. |
| **Dallas** | **Area 30** | Branch area; internal VLAN networks. |
| **Miami** | **Area 40** | Branch area; internal VLAN networks. |
| **Ashburn (DR)**| **Area 50** | DR site area; internal VLANs and infrastructure. |

![OSPF](screenshots/ospf-areas.png)

---

## Router ID Assignment

Router IDs are statically assigned using dedicated Loopback interfaces to ensure stability, regardless of physical interface state changes.

### Headquarters (Area 0)
| Device | Router ID |
| :--- | :--- |
| HQ-R1 | `10.255.10.11` |
| HQ-R2 | `10.255.10.12` |
| HQ-EDGE-1 | `10.255.10.1` |
| HQ-EDGE-2 | `10.255.10.2` |

### Branch Offices
| Location | Device | Router ID |
| :--- | :--- | :--- |
| **Chicago** | CHI-R1 | `10.255.20.1` |
| | CHI-R2 | `10.255.20.2` |
| **Dallas** | DAL-R1 | `10.255.30.1` |
| | DAL-R2 | `10.255.30.2` |
| **Miami** | MIA-R1 | `10.255.40.1` |
| | MIA-R2 | `10.255.40.2` |

### Ashburn DR Site (Area 50)
| Device | Router ID |
| :--- | :--- |
| ASH-R1 | `10.255.50.1` |
| ASH-R2 | `10.255.50.2` |
| ASH-INTERNAL-1 | `10.255.50.3` |
| ASH-INTERNAL-2 | `10.255.50.4` |

---

## Design Best Practices

### Passive Interfaces
User-facing SVI (Switched Virtual Interface) and access VLAN interfaces are configured as `passive-interface` in OSPF. 
- **Benefit:** Advertises the connected subnet into the OSPF domain without attempting to form unnecessary (and potentially insecure) neighbor adjacencies with endpoint devices.
- **Exception:** Transit interfaces and point-to-point links remain active to facilitate required neighbor relationships.

### Route Summarization
Where applicable, ABRs are configured to summarize branch subnets before advertising them into Area 0, reducing the size of the backbone routing table and limiting the scope of topology change notifications (Type 3 LSAs).

---

## Protocol Interactions & Boundaries

OSPF does not operate in a vacuum. Its behavior is carefully coordinated with other network protocols:

- **OSPF & Firewall HA:** The Meridian firewall architecture uses an Active/Standby HA design. The firewall pair participates in OSPF as a single logical routing endpoint (using the HA virtual IP/mac). OSPF verification focuses on the adjacency to this logical entity, not the individual physical chassis.
- **OSPF & HSRP:** HSRP provides First-Hop Redundancy (FHRP) for local VLAN default gateways, while OSPF handles dynamic routing *between* those routed segments. They operate at different layers of the forwarding path. *(See: `Routing/verification/hsrp-verification.md`)*
- **OSPF & BGP:** Strict separation of concerns. OSPF manages the internal IGP domain. BGP is reserved for External Gateway Protocol (EGP) tasks, such as ISP peering and hybrid cloud connectivity. Route redistribution between the two is strictly controlled and filtered. *(See: `Routing/BGP/`)*

---

## Configuration & Verification

To maintain a clean separation of concerns, implementation details and testing evidence are organized into dedicated sub-directories:

### Configuration
- [Single-Area OSPF Implementation](single-area/README.md) *(if applicable)*
- [Multi-Area OSPF Implementation](multi-area/README.md)

### Operational Verification
Comprehensive steady-state and functional failure testing is documented separately to prove resiliency.
- **Documentation:** [`Routing/verification/ospf-verification.md`](verification/ospf-verification.md)
- **Verification Scope:** Neighbor adjacency states, Router ID validation, Area assignments, LSDB integrity, path selection, and convergence behavior during intentional link/node failures.
