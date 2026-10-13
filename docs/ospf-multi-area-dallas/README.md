# Multi-Area OSPF – Dallas (Area 30)

## Overview
Dallas site is configured in **OSPF Area 30** and connected to the HQ backbone (**Area 0**) via two ABRs (DAL-R1 and DAL-R2) for redundancy.

- **Area 30**: All Dallas internal networks (10.30.0.0/16 range)
- **Area 0**: Links toward New York Headquarters
- OSPF Process ID: 10
- Router-IDs: 10.255.30.1 (DAL-R1) / 10.255.30.2 (DAL-R2)

## Configuration Summary
- Passive interfaces on access/VLAN subinterfaces
- Network statements for all Dallas VLANs in Area 30
- Uplink networks placed in Area 0

## Verification Results

### Neighbor Adjacencies
![OSPF Neighbors](screenshots/01-ospf-neighbors.png)

Both DAL routers form FULL adjacencies with each other and with HQ.

### ABR Status

DAL-R1 and DAL-R2 are correctly recognized as Area Border Routers.

### Routing Table
![Routing Table](screenshots/03-routing-table.png)

- Intra-area routes (O) for local Dallas networks
- Inter-area routes (O IA) for HQ and other remote sites

### Connectivity Tests
- Intra-area (Dallas ↔ Dallas): Successful
- Inter-area (Dallas ↔ HQ): Successful

![Inter-area Ping](screenshots/04-inter-area-ping.png)
![Traceroute](screenshots/05-traceroute.png)

## Conclusion
Multi-area OSPF for Dallas (Area 30) is fully operational. Routes are correctly exchanged with Area 0 via the dual ABRs, and end-to-end connectivity has been verified.
