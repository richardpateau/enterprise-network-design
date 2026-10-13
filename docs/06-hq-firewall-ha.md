# HQ Firewall Failover and OSPF

Purpose:
Provide an Active/Standby firewall pair so the DMZ gateway and HQ routing
stay available if one firewall fails.

Failover:
- HQ-FW-1 = Primary / Active
- HQ-FW-2 = Secondary / Standby
- Failover link = GigabitEthernet0/5
- DMZ active IP = 10.10.80.1
- DMZ standby IP = 10.10.80.2
- Server gateway = 10.10.80.1

OSPF:
- Firewalls form OSPF neighbors with HQ-R1 / HQ-R2 / HQ-EDGE-1 / HQ-EDGE-2
- After failover, the new Active keeps/rebuilds the adjacencies

Published service:
- DMZ web = 10.10.80.10
- Public NAT = 198.18.0.50
