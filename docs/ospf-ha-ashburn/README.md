# Ashburn (Area 50) – Multi-Area OSPF + HA Firewall

## Overview
Ashburn site runs **OSPF Area 50** connected to HQ Area 0 via dual ABRs (ASH-R1 / ASH-R2).  
The site also has an Active/Standby HA firewall pair (ASH-FW-1 / ASH-FW-2).

## OSPF Verification
- Area 50 (Ashburn) ↔ Area 0 (HQ)
- Dual ABRs for redundancy
- Inter-area routes (O IA) present on both sides

![OSPF Neighbors](screenshots/01-ospf-neighbors.png)  
![Border Routers](screenshots/02-border-routers.png)  
![Routing Table](screenshots/03-routing-table.png)

### Connectivity
- Intra-area: Successful  
- Inter-area (Ashburn ↔ HQ): Successful

![Inter-area Ping](screenshots/04-inter-area-ping.png)  
![Traceroute](screenshots/05-traceroute.png)

## HA Firewall Failover
Active/Standby HA is configured on ASH-FW-1 and ASH-FW-2.

![Failover Status](screenshots/06-failover-status.png)  
![Failover History](screenshots/07-failover-history.png)

### Failover Test
Continuous traffic was running while the Active firewall was failed over.  
Traffic recovered with minimal packet loss and the Standby unit became Active.

![Failover Ping Test](screenshots/08-failover-ping-test.png)

## Conclusion
- Multi-area OSPF for Ashburn (Area 50) is fully operational with dual ABRs.  
- HA firewall failover was successfully tested and verified.
