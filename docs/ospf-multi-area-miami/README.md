# Multi-Area OSPF – Miami (Area 40)

## Overview
Miami site is configured in **OSPF Area 40** and connected to the HQ backbone (**Area 0**) via two ABRs (MIA-R1 and MIA-R2) for redundancy.

- **Area 40**: All Miami internal networks
- **Area 0**: Uplinks toward New York Headquarters
- OSPF Process ID: 10 (or your process ID)
- Dual ABRs for high availability

## Configuration Summary
- Passive interfaces on access / VLAN interfaces
- Network statements for Miami subnets in Area 40
- Uplink networks placed in Area 0

## Verification Results

### Neighbor Adjacencies
![OSPF Neighbors](screenshots/01-ospf-neighbors.png)

Both Miami routers form FULL adjacencies with each other and with HQ.

### ABR Status
![Border Routers](screenshots/02-border-routers.png)

MIA-R1 and MIA-R2 are correctly acting as Area Border Routers.

### Routing Table
![Routing Table](screenshots/03-routing-table.png)

- Intra-area routes (O) for local Miami networks  
- Inter-area routes (O IA) for HQ and remote sites

### Connectivity Tests
- Intra-area (Miami ↔ Miami): Successful  
- Inter-area (Miami ↔ HQ): Successful

![Inter-area Ping](screenshots/04-inter-area-ping.png)  
![Traceroute](screenshots/05-traceroute.png)

## Conclusion
Multi-area OSPF for Miami (Area 40) is fully operational. Routes are correctly exchanged with Area 0 via the dual ABRs, and end-to-end connectivity has been verified.
