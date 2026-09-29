# Multi-Area OSPF – HQ (New York) ↔ CHI (Chicago)

## Overview
Multi-area OSPF was configured between New York Headquarters and the Chicago site to provide scalable and hierarchical routing.

- **HQ** → OSPF Area 0 (Backbone)
- **CHI** → OSPF Area 10
- ABRs: HQ-EDGE-1 / HQ-EDGE-2 (or HQ-R1/HQ-R2)

## Topology
![Topology](../topology.png)

## Configuration Summary
- Process ID: 1
- Area 0: All HQ core/edge routers
- Area 10: CHI-R1, CHI-R2 and connected switches
- Network statements / interface-based OSPF used
- Passive interfaces on access ports

## Verification

### Neighbor Adjacencies
![OSPF Neighbors](screenshots/01-ospf-neighbors.png)

All expected neighbors are in **FULL** state.

### OSPF Database & Routes
![OSPF Database](screenshots/02-ospf-database.png)
![Routing Table](screenshots/03-routing-table.png)

Inter-area routes (O IA) are present on both sides.

### Connectivity Tests
- Intra-area (CHI ↔ CHI): Successful
- Inter-area (CHI ↔ HQ): Successful

![Inter-area Ping](screenshots/04-inter-area-ping.png)
![Traceroute](screenshots/05-traceroute.png)

## Conclusion
Multi-area OSPF is fully operational. Routes are correctly exchanged between Area 0 and Area 10 via the ABRs, and end-to-end connectivity has been verified.
