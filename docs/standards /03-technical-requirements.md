# Technical Requirements

## Routing

### OSPF

- OSPF will be used as the enterprise Interior Gateway Protocol (IGP).
- OSPF will provide internal routing between HQ, branch, and DR networks.
- OSPF will provide dynamic route convergence following link or device failures.

### BGP

- eBGP will be used at the Internet edge for ISP connectivity.
- The HQ Internet edge will use two ISP connections.
- BGP will provide Internet-path redundancy during an ISP failure.

## IP Addressing

### IPv4

- The enterprise will use a structured private IPv4 addressing scheme.
- IP addressing will be documented in NetBox.
- Address space will be allocated by site, VLAN, and network function.

### IPv6

- IPv6 will be implemented on selected enterprise network segments.
- IPv6 addressing will follow a structured addressing plan.
- IPv6 routing and connectivity will be validated independently from IPv4.

## LAN

### VLAN Segmentation

The HQ and branch LANs will use VLAN segmentation to separate
different types of traffic.

Planned segmentation includes:

- Corporate users
- Voice
- Servers
- Management
- Guest
- IoT / Printers

### HSRP

- HSRP will provide default-gateway redundancy at the HQ core.
- Core-1 and Core-2 will provide redundant first-hop connectivity.

### LACP

- LACP will be used where multiple physical links are bundled into
  logical connections.
- LACP will provide increased bandwidth and link-level redundancy.

### STP

- STP will prevent Layer 2 switching loops.
- STP behavior will be designed around the redundant core/access topology.

## Security

### Firewalls

- Firewalls will provide the primary security boundary between the
  enterprise network and external networks.
- The HQ firewall infrastructure will use a high-availability design.

### IPsec

- Site-to-site IPsec VPNs will provide backup connectivity between
  sites.
- Remote-access IPsec VPN will provide secure connectivity for
  authorized remote users.

### ISE

Cisco ISE will provide centralized network-access authentication and
authorization.

Planned use cases include:

- 802.1X authentication
- Device/user authentication
- Network access authorization
- Guest access
- Policy-based access control

## Documentation

### NetBox

NetBox will serve as the network source of truth.

NetBox will document:

- Sites
- Devices
- Interfaces
- IP addresses
- Prefixes
- VLANs
- VRFs
- WAN circuits
- Network connections

## Monitoring

### SolarWinds

SolarWinds will provide centralized infrastructure monitoring.

The monitoring platform will monitor:

- Device availability
- Interfaces
- CPU
- Memory
- Utilization
- Packet loss
- Latency
- Routing neighbors

### SIEM

A centralized SIEM will collect and analyze security and operational
events from network infrastructure.

### Wireshark

Wireshark will be used for packet-level troubleshooting and validation.

It will be used to verify:

- VLAN behavior
- Routing behavior
- IPsec traffic
- Application traffic
- QoS behavior
- Packet loss
- Network failures


## Technical Success Criteria

The implementation will be considered technically successful when:

- OSPF provides internal routing and converges after failures.
- BGP provides redundant ISP connectivity.
- IPv4 and IPv6 connectivity are operational.
- VLAN segmentation is implemented and validated.
- HSRP provides first-hop redundancy.
- LACP provides link redundancy where implemented.
- STP prevents Layer 2 loops.
- Firewalls provide the required security boundaries.
- Site-to-site and remote-access VPNs function correctly.
- ISE provides centralized authentication and authorization.
- NetBox accurately documents the deployed network.
- SolarWinds provides infrastructure monitoring.
- SIEM receives centralized events.
- Wireshark can validate network behavior.
