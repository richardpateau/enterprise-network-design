# HQ Dual-ISP Failover

Purpose:
Keep internet reachability if ISP-A fails by shifting traffic to ISP-B.

Design:
- HQ-EDGE-1 = ISP-A
- HQ-EDGE-2 = ISP-B
- Prefer ISP-A (higher local-pref / better AD)
- Core/firewall next hop stays stable (HSRP or OSPF)
- Test target: 203.0.113.10

Normal path:
PC1 → 10.10.10.2 → HQ-FW-1 (10.255.110.2) → EDGE-1 → ISP-A → 203.0.113.10

Failure test:
Shut HQ-EDGE-1 interface to ISP-A.
Expected: BGP/static to A drops, traffic uses EDGE-2 → ISP-B.
Expected result: ping to 203.0.113.10 still succeeds and traceroute middle hops change.
