# Meridian Financial Services — Enterprise IPv6 Dual-Stack Implementation

> **Portfolio Lab Project.** This documentation details the manual design, configuration, and troubleshooting of an enterprise-wide IPv6 migration within the fictional "Meridian Financial Services" multi-site topology (PNETLab). 

## Summary

The objective of this project was to extend Meridian's existing IPv4 enterprise network (HQ, Chicago, Dallas, Miami, and Ashburn DR) to support IPv6 using a dual-stack approach. 

Rather than simply enabling IPv6, this project focuses on the operational realities of an enterprise migration: implementing **OSPFv3 Address Families**, configuring **IPv6 HSRP** for gateway redundancy, deploying **SLAAC and DHCPv6 (Stateless/Stateful/Relay)** for host provisioning, and securing the network against **Rogue Router Advertisements** using Layer 3 ACLs.

---

## ️ Network Topology

The implementation spans a multi-region enterprise topology:
*   **New York HQ:** Core routing, DHCPv6 services, and HSRP gateways.
*   **Branch Sites:** Chicago, Dallas, Miami, and Ashburn (Area 50).
*   **Addressing Convention:** Site-coded documentation prefixes (e.g., HQ uses `2001:DB8:10::/48`, Dallas uses `2001:DB8:30::/48`).

![ipv6](screenshots/topology.png)

---

## What was built
 
| Area | Summary | Status |
|---|---|---|
| Addressing | Site-coded `/48` per site, `/64` per VLAN, `/128` loopbacks | Working; spreadsheet/Nautobot still to reconcile |
| OSPFv3 | Process 10, FULL adjacencies on HQ-EDGE-1 and HQ-FW-1; client VLANs passive | Neighbors observed; cross-site reachability to capture |
| IPv6 HSRP | HQ-R1 (priority 110, preempt) / HQ-R2 on VLANs 10-70, virtual link-local gateways (e.g. `FE80::30` on VLAN 30) | Configured; failover test to capture |
| SLAAC / RA | RA interval 30s, router lifetime 90s, prefix 86400/14400 on HQ VLANs | Working; packet captures done |
| Stateless DHCPv6 | `MERIDIAN-STATELESS` on HQ-R1 (O flag): SLAAC address plus DNS/domain via Information-request/Reply | Working; captures done |
| Stateful DHCPv6 | `MERIDIAN-STATEFUL-VLAN30` on HQ VLAN 30 (M flag, `no-autoconfig`) | Client lease obtained |
| Branch DHCPv6 relay | VLAN 30 relays to HQ-R1; per-site pools selected by `link-address` | Relay forwarding confirmed; lease end-to-end still to confirm (see troubleshooting) |
| IPv6 ACL | `MERIDIAN-VLAN30-IN` on VLAN 30 (RA deny, ICMPv6, DHCPv6, HSRP, default deny with logging) | Counters observed |
| Duplicate Address Detection | Captured and explained | Done |
 
## Addressing
 
| Site | Prefix | Example VLAN 30 |
|---|---|---|
| HQ | `2001:DB8:10::/48` | `2001:DB8:10:30::/64` |
| Chicago | `2001:DB8:20::/48` | `2001:DB8:20:30::/64` |
| Dallas | `2001:DB8:30::/48` | `2001:DB8:30:30::/64` |
| Miami | `2001:DB8:40::/48` | `2001:DB8:40:30::/64` |
| Ashburn DR | `2001:DB8:50::/48` | `2001:DB8:50:30::/64` |

## Implementation & Evidence

### 1. OSPFv3 and Dual-Stack Routing
OSPFv3 was configured using Address Families to maintain a unified routing process for both IPv4 and IPv6. Adjacencies were established across the core and branch links, keeping client VLAN SVIs passive while forming FULL neighbor states on transit links.

```cisco
interface FastEthernet0/0.<VLAN>
 ipv6 10 area < area # >
```

![Automation](screenshots/area-number.png)

**show ipv6 ospf neighbor**

![Automation](screenshots/area-number.png)

**show ipv6 route**

![ipv6](screenshots/sh-ipv6-route-ospf-1.png)

![ipv6](screenshots/sh-ipv6-route-ospf-2.png)

### 2. High Availability (IPv6 HSRP)
To ensure gateway resilience, IPv6 HSRP was deployed on the HQ-R1/HQ-R2 gateway pair for VLANs 10–70. 
*   **Design:** HQ-R1 acts as Active (Priority 110), HQ-R2 as Standby (Priority 100).
*   **Virtual Gateway:** Uses a Link-Local Virtual IP (`FE80::1`) per VLAN group.
*   **Example Configuration:**

```cisco
interface FastEthernet0/0.30
 standby version 2
 standby 130 ipv6 FE80::30
 standby 130 priority 110      ! HQ-R2 uses the default (100)
 standby 130 preempt
```
**HQ-R1**

![Automation](screenshots/sh-standby-brief-r1.png)

**HQ-R2**

![Automation](screenshots/sh-standby-brief-r2.png)

### 3. Host Provisioning (SLAAC & DHCPv6)
A hybrid approach was used to demonstrate different IPv6 host configuration methods:
*   **SLAAC + Stateless DHCPv6:** Used for general HQ VLANs. Hosts auto-configure their IPv6 address via Router Advertisements (RA) and use DHCPv6 solely for DNS and Domain Name options (O-flag set).

```cisco
ipv6 dhcp pool MERIDIAN-STATELESS
 dns-server 2001:DB8:10:FFFD::3
 domain-name meridian.local
!
interface FastEthernet0/0.<VLAN>
 ipv6 nd other-config-flag
 ipv6 dhcp server MERIDIAN-STATELESS
```
*   **Stateful DHCPv6:** Configured on HQ VLAN 30. The Managed-config-flag (M-flag) is set, and SLAAC is disabled (`no-autoconfig`), forcing hosts to obtain their IPv6 address entirely from the DHCPv6 server.

```cisco
ipv6 dhcp pool MERIDIAN-STATEFUL-VLAN30
 address prefix 2001:DB8:10:30::/64 lifetime 86400 14400
 dns-server 2001:DB8:10:FFFD::3
 domain-name meridian.local
!
interface FastEthernet0/0.30
 ipv6 dhcp server MERIDIAN-STATEFUL-VLAN30
 ipv6 nd managed-config-flag
 no ipv6 nd other-config-flag
 ipv6 nd prefix 2001:DB8:10:30::/64 86400 14400 no-autoconfig
```

The M flag plus `no-autoconfig` means clients get addresses from DHCPv6 only, not SLAAC.

**R1 Configured with an IPv6 Prefix**

![Automation](screenshots/slaac-r1-config.png)

**Switch: Assigning VLAN 20 to switchport**

![Automation](screenshots/slaac-switch-config.png)

**PC1 configuring IPv6 address via SLAAC**

![Automation](screenshots/slaac-pc-1-gets-ip.png)

**PCAP: icmpv6.type == 133 || icmpv6.type == 134**

![Automation](screenshots/slaac-pcap-overview.png)

**PCAP: RA Details**

![Automation](screenshots/slaac-pcap-details.png)

**Stateless DHCP Configuration**

![Automation](screenshots/stateless-config-r1.png)

**PC obtains IP via Stateless DHCPv6**

![ipv6](screenshots/stateless-pc-gets-config.png)

**PCAP: Stateless DHCPv6 Information Requests**

![ipv6](screenshots/slaac-pcap-details.png)

**PCAP: Stateless DHCPv6 Information Reply**

![ipv6](screenshots/stateless-pcap-information-reply.png)

### 3.1. Duplicate Address Detection (DAD)
IPv6 uses Duplicate Address Detection to ensure address uniqueness before assignment. When a host generates an address (via SLAAC or other means), it sends Neighbor Solicitation messages to the solicited-node multicast address to verify no other host is using that address.

**DAD Packet Capture Evidence:**
The Wireshark captures show ICMPv6 Type 135 (Neighbor Solicitation) messages sent to `ff02::1:ff00:5800` (solicited-node multicast) with the Target Address field containing the address being validated.

![ipv6](screenshots/dad-pcap-overview.png)

![ipv6](screenshots/dad-pcap-details.png)

**Tip:** The raw packet captures for SLAAC, Stateless DHCPv6, Stateful DHCPv6, and Rogue RA testing are available in the [`pcaps/`](pcaps/) directory of this repository for hands-on Wireshark analysis.

**

### 3. Host Provisioning (SLAAC & DHCPv6)

*   **Stateful DHCPv6:** Configured on HQ VLAN 30. The Managed-config-flag (M-flag) is set, and SLAAC is disabled (`no-autoconfig`), forcing hosts to obtain their IPv6 address entirely from the DHCPv6 server.

**Stateful DHCP Pool Configuration**

![Automation](screenshots/stateful-dhcp-pool.png)

**Stateful DHCP Assigned to Interface**

![Automation](screenshots/Stateful-dhcp-r1-config.png)

**Switching Access VLAN to 30**

![Automation](screenshots/stateful-switch-config.png)

**PC Successfulyl obtains IP via Stateful DHCP**

![Automation](screenshots/stateful-pc-1-gets-ip.png)

**PCAP: PC Successfulyl obtains IP via Stateful DHCP**

![Automation](screenshots/stateful-pcap-pc-gets-ip.png)

*   **DHCPv6 Relay:** Branch sites (Chicago, Dallas, Miami, Ashburn) utilize `ipv6 dhcp relay` to forward client requests to the centralized HQ-R1 DHCPv6 server, using link-address selectors to assign the correct site-specific pool.

![ipv6](screenshots/dhcp-relay-dal-r1.png)

### 4. Security: Rogue RA Mitigation (Layer 3 ACL)
Because the access switch image in this lab environment does not support Layer 2 RA Guard, a Layer 3 mitigation strategy was implemented on the router interface for VLAN 30. 
*   **Control:** The `MERIDIAN-VLAN30-IN` IPv6 ACL explicitly denies incoming Router Advertisements sourced from the link-local range (`FE80::/10`), while permitting essential ICMPv6, DHCPv6 (UDP 546/547), and HSRP (UDP 2029) traffic.

```cisco
ipv6 access-list MERIDIAN-VLAN30-IN
 sequence 10 deny icmp FE80::/10 any router-advertisement log
 sequence 20 permit icmp any any
 sequence 30 permit udp any eq 546 any eq 547       ! DHCPv6 client -> server/relay
 sequence 35 permit udp any eq 547 any eq 547       ! DHCPv6 relay <-> server
 sequence 40 permit udp any eq 2029 any eq 2029 
 sequence 50 permit ipv6 2001:DB8:10:30::/64 any
 sequence 60 deny ipv6 any any log
```
![ipv6](screenshots/acl-added-ra.png)

**Rogue Router: Assigning IPv6 fe80::bad:beef**

![ipv6](screenshots/acl-test-rogue-router.png)

**IPv6 ACL catches Rogue Router**

![ipv6](screenshots/acl-bad-ra-syslog.png)

**PCAP: RA's Sent**

![ipv6](screenshots/dad-rogue-ra-pcap.png)

### 5. External BGP (eBGP) and Traffic Engineering
To connect the Meridian network to external providers, a dual-stack BGP implementation was deployed on the edge routers (HQ-EDGE-1 and HQ-EDGE-2).
*   **Dual-Stack Address Families:** BGP is configured with separate `address-family ipv4` and `address-family ipv6` blocks, peering with ISP-A (AS 65001) and ISP-B (AS 65002) over both IPv4 and IPv6 transit links.
*   **iBGP Peering:** HQ-EDGE-1 and HQ-EDGE-2 establish an iBGP session (AS 65000) using Loopback interfaces for stability, with `next-hop-self` configured for the IPv6 address family to ensure proper reachability.
*   **Inbound Traffic Engineering:** A route-map (`ISP-A-IN`) is applied to the ISP-A neighbor to set the `local-preference` to 200. This ensures that Meridian prefers ISP-A as the primary exit and entry point for traffic.
*   **Controlled Redistribution:** External BGP routes are carefully redistributed into the internal OSPF/OSPFv3 domain using a prefix-list (`BGP-TO-OSPF-PREFIX`) and route-map (`FILTER-BGP-INTO-OSPF`) to prevent default routes or unwanted external prefixes from flooding the internal routing table.

```cisco
route-map ISP-A-IN permit 10
 set local-preference 200
```

![ipv6](screenshots/sh-run-section-bgp.png)

![ipv6](screenshots/sh-bgp-summary.png)
---

##  Repository Structure

*   `README.md` - This master documentation file.
*   `screenshots/` - Contains all CLI outputs, Wireshark packet captures, and topology diagrams referenced above.

---
