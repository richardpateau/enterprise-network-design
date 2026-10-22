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

---

## ⚙️ Implementations

### 1. OSPFv3 and Dual-Stack Routing
OSPFv3 was configured using Address Families to maintain a unified routing process for both IPv4 and IPv6. Adjacencies were established across the core and branch links, keeping client VLAN SVIs passive while forming FULL neighbor states on transit links.

### 2. High Availability (IPv6 HSRP)
To ensure gateway resilience, IPv6 HSRP was deployed on the HQ-R1/HQ-R2 gateway pair for VLANs 10–70. 
*   **Design:** HQ-R1 acts as Active (Priority 110), HQ-R2 as Standby (Priority 100).
*   **Virtual Gateway:** Uses a Link-Local Virtual IP (`FE80::1`) per VLAN group.

```cisco
interface FastEthernet0/0.<VLAN>
 no ipv6 nd ra suppress
 ipv6 nd ra interval 30
 ipv6 nd ra lifetime 90
 ipv6 nd prefix 2001:DB8:10:<VLAN>::/64 86400 14400
```

### 3. Host Provisioning (SLAAC & DHCPv6)
A hybrid approach was used to demonstrate different IPv6 host configuration methods:
*   **SLAAC + Stateless DHCPv6:** Used for general HQ VLANs. Hosts auto-configure their IPv6 address via Router Advertisements (RA) and use DHCPv6 solely for DNS and Domain Name options (O-flag set).
*   **Stateful DHCPv6:** Configured on HQ VLAN 30. The Managed-config-flag (M-flag) is set, and SLAAC is disabled (`no-autoconfig`), forcing hosts to obtain their IPv6 address entirely from the DHCPv6 server.
*   **DHCPv6 Relay:** Branch sites (Chicago, Dallas, Miami, Ashburn) utilize `ipv6 dhcp relay` to forward client requests to the centralized HQ-R1 DHCPv6 server, using link-address selectors to assign the correct site-specific pool.

### 4. Security: Rogue RA Mitigation (Layer 3 ACL)
Because the access switch image in this lab environment does not support Layer 2 RA Guard, a Layer 3 mitigation strategy was implemented on the router interface for VLAN 30. 
*   **Control:** The `MERIDIAN-VLAN30-IN` IPv6 ACL explicitly denies incoming Router Advertisements sourced from the link-local range (`FE80::/10`), while permitting essential ICMPv6, DHCPv6 (UDP 546/547), and HSRP (UDP 2029) traffic.


---

## 📸 Implementation Evidence

### A. SLAAC and Neighbor Discovery
Hosts on VLAN 20 successfully obtain IPv6 addresses via SLAAC. Packet captures confirm standard ICMPv6 Type 133 (Router Solicitation) and Type 134 (Router Advertisement) exchanges, including Duplicate Address Detection (DAD).

| SLAAC Client Address | Router Solicitation (Type 133) | RA Details & Prefix Info |
|---|---|---|
| ![SLAAC Client](screenshots/slaac%20pc%201%20getting%20ip%20from%20vlan%2020%20.png) | ![RS Packet](screenshots/SLAAC%20PCAP%20ROUTER%20SOLICITATION%20OVERVIEW.png) | ![RA Details](screenshots/SLAAC%20RA%20DETAILS.png) |

| DAD Packet Overview | Switch Port VLAN Assignment |
|---|---|
| ![DAD Overview](screenshots/DAD%20packet%20overview.png) | ![Switch VLAN](screenshots/SWITCH%20DURING%20SLAAC%20TESTING%20By%20changing%20port%20to%20access%20vlan%2020.png) |

### B. DHCPv6: Stateless and Stateful
**Stateless DHCPv6:** The `MERIDIAN-STATELESS` pool provides DNS and domain information to SLAAC-enabled hosts.

| Pool Configuration | Information Request (Wireshark) | Information Reply (DNS Details) |
|---|---|---|
| ![Stateless Config](screenshots/DHCP%20STATELESSS%20sh%20run%20section%20dhcp%20R1.png) | ![Info Request](screenshots/pcap%20wireshark%20filrer%20dhcpv6%20information%20request%20stateless.png) | ![Info Reply](screenshots/pcap%20wireshark%20information%20reply%20stateless%20with%20dns%20details.png) |

**Stateful DHCPv6 (VLAN 30):** The `MERIDIAN-STATEFUL-VLAN30` pool assigns actual IPv6 addresses.

| Stateful Config on R1 | Client Receiving Stateful Address |
|---|---|
| ![Stateful Config](screenshots/testing%20Stateful%20conifg%20R1%20sh%20int%20f0-0.30%20configuration.png) | ![Stateful Client](screenshots/PC%203%20gaining%20a%20stateful%20DHCP%20ipv6%20address.png) |

### C. Security: IPv6 ACL Rogue RA Filtering
To mitigate rogue routers, an IPv6 ACL (`MERIDIAN-VLAN30-IN`) was applied to the VLAN 30 interface. The ACL successfully matches and drops unauthorized Router Advertisements while maintaining counters.

| ACL Configuration & Counters |
|---|
| ![IPv6 ACL RA Filter](screenshots/IPV6%20ACL%20added%20for%20RA.png) |

*Note: The ACL sequence 10 explicitly denies `icmp FE80::/10 any router-advertisement log`. The counter shows 362 matches, confirming the filter is actively protecting the segment.*

---


##  Repository Structure

*   `README.md` - This master documentation file.
*   `screenshots/` - Contains all CLI outputs, Wireshark packet captures, and topology diagrams referenced above.

---
