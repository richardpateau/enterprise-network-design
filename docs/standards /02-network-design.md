# Meridian Financial Services
## High-Level Network Design

## 1. Design Goals

### Scalability

The network will support approximately 1,200 users across four corporate
locations, with an architecture capable of scaling toward 2,000 users without
requiring a complete redesign.

### High Availability

Critical network services will be designed with redundancy to minimize the
impact of individual device, link, or ISP failures.

### Secure Connectivity

Communication between corporate sites and remote users will use secure,
encrypted connectivity where required.

### Segmentation

Users, voice, servers, guests, management, and other network resources will
be logically separated to limit unnecessary access and reduce the impact of
security incidents.

### Reliable Routing

OSPF will provide internal routing across the enterprise, while BGP will be
used for external connectivity and ISP redundancy.

### Internet Redundancy

The headquarters will use multiple Internet providers to provide connectivity
during an individual ISP failure.

### Identity-Based Access

Network access will be controlled using centralized authentication and
authorization. Cisco ISE will provide identity-based access control for
supported network access scenarios.

### Centralized Management

Network infrastructure will be documented using NetBox as the source of truth
and monitored using centralized network-management and logging platforms.

### Disaster Recovery

Critical services will have a recovery capability at the Ashburn DR/Data
Center facility in the event that the primary environment becomes unavailable.

### Operational Visibility

The network will provide centralized monitoring, logging, and troubleshooting
capabilities so that failures and performance problems can be detected and
investigated.

### Automation Readiness

The network will be designed with consistent addressing, naming, and device
configuration practices so that portions of the infrastructure can later be
automated using Python, Ansible, and NetBox.
## 2. Site Architecture

Meridian Financial Services will use a five-site architecture consisting of one
headquarters, three regional branch offices, and one disaster recovery/data
center facility.

### New York HQ

New York will serve as the primary headquarters and largest corporate site.

The site will contain:

- Redundant core routing infrastructure
- Distribution and access switching
- Redundant Internet connectivity
- Firewalls
- Corporate user networks
- Voice services
- Server and management networks
- Guest network
- Network management and monitoring infrastructure

New York will serve as the primary corporate network hub.

### Chicago Branch

Chicago will serve as a regional office supporting approximately 300 users.

The site will contain:

- WAN edge routing
- Access switching
- Corporate user networks
- Voice network
- Guest network
- Management network
- Local Internet/WAN connectivity

Chicago will maintain connectivity to HQ and critical services hosted at the
DR/Data Center.

### Dallas Branch

Dallas will support approximately 200 users.

The site will contain:

- WAN edge routing
- Access switching
- Corporate user networks
- Voice network
- Guest network
- Management network
- WAN connectivity to corporate resources

### Miami Branch

Miami will support approximately 200 users.

The site will contain:

- WAN edge routing
- Access switching
- Corporate user networks
- Voice network
- Guest network
- Management network
- WAN connectivity to corporate resources

### Ashburn DR/Data Center

Ashburn will serve as the organization's disaster recovery and data center
facility.

The site will contain:

- Redundant network connectivity
- Critical application servers
- Authentication services
- DNS/DHCP services
- Monitoring and logging infrastructure
- Backup services
- Management infrastructure

Ashburn will provide recovery capabilities for critical services if the
primary HQ environment becomes unavailable.

### Site Connectivity

All corporate sites will have secure connectivity to HQ and the DR/Data
Center.

The architecture will use:

- OSPF for internal routing
- BGP for external/WAN routing and ISP redundancy
- IPsec VPN for secure site-to-site connectivity where required
- Redundant paths for critical locations

## 3. WAN Architecture

The Meridian Financial Services WAN will provide secure and redundant
connectivity between the New York headquarters, regional branch offices, and
the Ashburn disaster recovery/data center facility.

### WAN Design Goals

The WAN must:

- Provide reliable connectivity between all corporate sites.
- Provide secure connectivity for inter-site traffic.
- Provide redundancy for critical WAN connections.
- Support automatic failover when a primary WAN path becomes unavailable.
- Allow the network to scale as additional sites are added.
- Provide centralized visibility into WAN performance and availability.

### Site Connectivity

New York HQ will serve as the primary corporate network hub.

The regional offices in Chicago, Dallas, and Miami will maintain WAN
connectivity to the corporate network and critical services hosted at the
Ashburn DR/Data Center.

The Ashburn facility will maintain connectivity to HQ and will provide a
secondary location for critical services.

### WAN Routing

OSPF will be used as the internal gateway protocol (IGP) for routing between
enterprise routers and internal network infrastructure.

BGP will be used at the external network boundary to provide connectivity to
Internet service providers and support ISP redundancy.

The routing responsibilities will therefore be separated as follows:

- OSPF: Internal enterprise routing
- BGP: External/Internet routing and ISP redundancy

### WAN Redundancy

Each corporate branch will have two WAN paths to provide connectivity to the
enterprise network.

The primary WAN path will be preferred during normal operation. A secondary
WAN path will remain available as a backup and will be used if the primary
path fails.

The WAN will therefore provide path redundancy without requiring both paths
to carry equal amounts of traffic during normal operation.

Each branch will have:

- Primary WAN path
- Secondary WAN path
- Dynamic routing over the available paths
- Automatic failover
- Monitoring of WAN-path availability

### WAN Path Selection

The network will use routing metrics and policy to establish a preferred
primary path.

During normal operation:

    Branch
       |
       | Primary Path
       v
      HQ

If the primary path fails:

    Branch
       |
       X Primary Path
       |
       | Secondary Path
       v
      HQ

Routing will reconverge and use the secondary path.

### WAN Failure Testing

Each branch will undergo controlled failure testing.

Testing will include:

1. Verify connectivity over the primary path.
2. Disable the primary WAN path.
3. Verify routing convergence.
4. Verify traffic uses the secondary path.
5. Restore the primary path.
6. Verify the network returns to the preferred path.

The failure and recovery process will be documented using routing tables,
routing-protocol status, monitoring alerts, and packet captures where
appropriate.

### Internet Connectivity

The New York headquarters will use two Internet service providers.

The Internet edge will use redundant edge routers and BGP sessions to provide
external routing and ISP failover.

Normal operation will prefer the primary ISP. If the primary ISP becomes
unavailable, traffic will be redirected through the secondary ISP.

### Site-to-Site VPN

IPsec site-to-site VPN tunnels will provide encrypted connectivity between
sites where required.

VPN connectivity will protect traffic traversing networks that are not
directly controlled by Meridian Financial Services.

The VPN design will support:

- HQ-to-branch connectivity
- HQ-to-DR connectivity
- Branch-to-DR connectivity where required

### WAN Failure Requirements

The WAN design will be tested against controlled failures including:

- Primary WAN link failure
- ISP failure
- Router failure
- IPsec tunnel failure

The expected result is that critical sites retain connectivity through an
available alternate path.

### WAN Monitoring

WAN links will be monitored for:

- Availability
- Utilization
- Latency
- Packet loss
- Interface errors
- Routing-neighbor status

WAN events will be reported through the centralized monitoring and logging
infrastructure.

### WAN Architecture Summary

The WAN will use a combination of OSPF, BGP, and IPsec:

OSPF provides internal route exchange and convergence.

BGP provides external routing and redundant Internet connectivity.

IPsec provides encrypted site-to-site communication across external or
untrusted networks.

## 4. Internet Edge

The New York headquarters will provide the primary Internet edge for
Meridian Financial Services. The Internet edge will use two independent
Internet service providers to provide redundancy and reduce the risk of a
single ISP failure.

### Internet Service Providers

Meridian will use two Internet providers:

- ISP-A: Primary Internet provider
- ISP-B: Secondary Internet provider

The two providers will connect to separate edge routers.

### Edge Routers

Two redundant edge routers will provide the connection between Meridian's
internal network and the Internet service providers.

The edge routers will:

- Establish external BGP sessions with the ISPs.
- Advertise approved enterprise prefixes.
- Receive appropriate Internet routes from the providers.
- Provide an alternate path if the primary ISP becomes unavailable.

### BGP

eBGP will be used between Meridian's edge routers and the Internet service
providers.

BGP will provide:

- External route exchange
- ISP redundancy
- Path selection
- Internet route control
- Automatic failover

The primary ISP will be preferred during normal operation. BGP policy will
allow traffic to use the secondary ISP if the primary ISP becomes
unavailable.

### Firewall Placement

The enterprise firewalls will be positioned between the Internet edge and the
internal corporate network.

The high-level traffic path will be:

    Internet
       |
    ISP-A / ISP-B
       |
    Edge Routers
       |
    Firewalls
       |
    Internal Network

The firewalls will enforce security policies between external and internal
networks.

### Security Zones

The Internet edge will separate traffic into logical security zones:

- OUTSIDE: Internet-facing traffic
- INSIDE: Corporate network
- DMZ: Public-facing services
- VPN: Remote-access and site-to-site VPN traffic
- MANAGEMENT: Restricted network-management traffic

### NAT

The firewalls will provide Network Address Translation for internal users
requiring Internet access.

The design will support:

- PAT for normal outbound user traffic
- Static NAT for approved public-facing services
- NAT policies appropriate for VPN traffic

### ISP Failure

The Internet edge will be tested by intentionally disabling the primary ISP
connection.

Normal operation:

    Internal Network
          |
       Firewall
          |
       Edge Router
          |
        ISP-A
          |
       Internet

After ISP-A failure:

    Internal Network
          |
       Firewall
          |
       Edge Router
          |
        ISP-B
          |
       Internet

BGP should detect the loss of the primary path and select the available
secondary path.

### Internet Edge Monitoring

The following components will be monitored:

- ISP connectivity
- BGP neighbor status
- Edge-router interfaces
- Firewall availability
- WAN utilization
- Packet loss
- Latency
- Interface errors

BGP and ISP failures will generate monitoring and logging events for
investigation.

### Internet Edge Design Goals

The Internet edge must:

- Provide redundant Internet connectivity.
- Protect the internal network from untrusted Internet traffic.
- Provide controlled access to public-facing services.
- Support secure remote-access and site-to-site VPN connectivity.
- Automatically fail over during an ISP failure.
- Provide sufficient monitoring and logging for troubleshooting.

## 5. LAN Architecture

The Meridian Financial Services LAN will use a hierarchical network design
consisting of core, distribution, and access layers. The architecture will
provide scalability, redundancy, segmentation, and centralized management.

### Core Layer

The core layer will provide high-speed Layer 3 connectivity between major
network segments and services.

At the New York headquarters, redundant core devices will be deployed to
reduce the impact of a single device failure.

The core will provide:

- Layer 3 routing
- Connectivity between distribution networks
- Connectivity to the data center and WAN
- OSPF routing
- Redundant paths
- HSRP gateway redundancy where appropriate

### Distribution Layer

The distribution layer will provide aggregation between the access layer and
the core.

Distribution devices will provide:

- VLAN gateway services
- Inter-VLAN routing
- Access-layer aggregation
- Security policy enforcement where appropriate
- Redundant uplinks to the core
- OSPF connectivity to the core

### Access Layer

The access layer will connect end-user devices to the corporate network.

Access switches will provide connectivity for:

- Employee workstations
- IP phones
- Printers
- IoT devices
- Wireless access points

Access ports will be assigned to the appropriate VLAN based on the device
and authorization policy.

### VLAN Segmentation

The LAN will use VLANs to logically separate different types of traffic.

The initial VLAN structure will include:

| VLAN | Purpose |
|---|---|
| 10 | Corporate Users |
| 20 | Voice |
| 30 | Servers |
| 40 | Guest |
| 50 | Management |
| 60 | Printers/IoT |
| 70 | Network Infrastructure |

Each VLAN will have its own IP subnet and default gateway.

### Inter-VLAN Routing

Inter-VLAN routing will be performed by Layer 3 network infrastructure.

Traffic between VLANs will be controlled according to security requirements.
Guest traffic will not be permitted to access internal corporate or server
networks.

### HSRP

Redundant Layer 3 devices at critical sites will use HSRP to provide a
virtual default gateway for internal VLANs.

Normal operation will use a preferred active device while a secondary device
remains available.

If the active gateway becomes unavailable, the standby device will assume the
virtual gateway address.

### EtherChannel / LACP

LACP will be used where multiple physical links connect network devices.

EtherChannel will provide:

- Increased available bandwidth
- Link redundancy
- Simplified logical topology

A failure of an individual physical link should not interrupt connectivity
when other members of the EtherChannel remain operational.

### Spanning Tree

Spanning Tree Protocol will protect the Layer 2 network from switching loops.

The design will establish predictable STP root placement and use appropriate
edge-port protections.

Access switches will use appropriate protections such as:

- PortFast
- BPDU Guard
- DHCP Snooping
- Dynamic ARP Inspection where appropriate

### Guest Network

Guest devices will be isolated from internal corporate networks.

Guest users will receive Internet access but will not be permitted to access:

- Corporate user networks
- Server networks
- Management networks
- Network infrastructure

### Management Network

Network infrastructure will use a dedicated management VLAN.

Management access will be restricted to authorized administrators and
management systems.

Network devices will use centralized authentication and authorization where
supported.

### Voice Network

IP phones will use a dedicated voice VLAN.

Voice traffic will be separated from normal user traffic and will be marked
appropriately for QoS treatment.

### Branch LAN Architecture

The branch offices will use a simplified version of the hierarchical design.

Each branch will contain:

- WAN edge routing
- Access switching
- User VLANs
- Voice VLAN
- Guest VLAN
- Management VLAN

Larger branches may use redundant Layer 3 distribution devices where
appropriate.

### LAN Design Goals

The LAN architecture will provide:

- Scalable user connectivity
- VLAN-based segmentation
- Redundant default gateways
- Redundant switch links
- Loop prevention
- Secure guest isolation
- Centralized management
- Consistent architecture across sites

## 6. Routing Architecture

The Meridian Financial Services network will use a hierarchical routing design.
OSPF will provide internal enterprise routing, while BGP will provide external
routing and Internet service-provider redundancy.

### Routing Protocol Roles

The routing responsibilities will be divided as follows:

- OSPF: Internal enterprise routing
- OSPFv3: Internal IPv6 routing
- BGP: External Internet routing and ISP redundancy
- HSRP: Default-gateway redundancy for internal VLANs

This separation allows each routing protocol to perform the function for which
it is best suited.

---

### OSPF Design

OSPF will be the primary interior gateway protocol (IGP) used throughout the
enterprise.

OSPF will provide:

- Internal route exchange
- Dynamic path selection
- Route convergence
- Primary and secondary WAN path selection
- Connectivity between sites
- Connectivity between the LAN, WAN, and data center

The OSPF topology will use a hierarchical area design.

### OSPF Areas

Area 0 will serve as the OSPF backbone.

Additional areas will be used to separate larger portions of the enterprise
network from the backbone.

The planned design is:

| Area | Location/Purpose |
|---|---|
| Area 0 | Core and backbone |
| Area 10 | New York HQ |
| Area 20 | Chicago |
| Area 30 | Dallas |
| Area 40 | Miami |
| Area 50 | Ashburn DR/Data Center |

Area boundaries will be placed at appropriate Layer 3 boundaries to allow
route summarization and limit unnecessary routing information.

---

### OSPF Path Selection

Each branch will have a primary and secondary WAN path.

OSPF interface costs will be used to establish the preferred path.

The primary WAN path will have a lower OSPF cost than the secondary path.

Example:

    Primary WAN path
    OSPF cost = 10

    Secondary WAN path
    OSPF cost = 100

Under normal conditions, traffic will use the primary path.

If the primary path fails, OSPF will remove the unavailable route and
converge toward the secondary path.

---

### OSPF Redundancy

The routing design will be tested by intentionally failing primary paths.

The expected behavior is:

    Normal:

    Branch
       |
       | Primary
       v
      HQ

    Primary failure:

    Branch
       |
       X Primary
       |
       | Secondary
       v
      HQ

OSPF should establish the alternate path without requiring manual route
changes.

---

### OSPF Route Summarization

Where appropriate, branch networks will be summarized at area boundaries.

Summarization will reduce the amount of routing information propagated
through the enterprise and provide greater scalability as additional
networks are added.

---

### OSPF Interface Configuration

Interfaces that do not require OSPF neighbor relationships will be configured
as passive where appropriate.

This prevents unnecessary OSPF adjacency formation while still allowing
connected networks to be advertised.

OSPF authentication will be used where appropriate to protect routing
adjacencies from unauthorized participation.

---

### BGP Architecture

BGP will be used at the Internet edge to exchange routes with the two
Internet service providers.

The high-level design is:

    ISP-A
      |
     eBGP
      |
    Edge-R1
      |
    Enterprise
      |
    Edge-R2
      |
     eBGP
      |
    ISP-B

BGP will provide:

- External route exchange
- ISP redundancy
- Internet path selection
- Route filtering
- Controlled advertisement of enterprise prefixes

---

### BGP Path Preference

ISP-A will be preferred during normal operation.

BGP policy will be used to influence path selection so that ISP-A is the
preferred provider.

ISP-B will provide a backup path.

If ISP-A becomes unavailable, BGP will withdraw the unavailable routes and
traffic will use ISP-B.

The project will demonstrate:

1. Both ISP connections operational.
2. ISP-A selected as the preferred path.
3. ISP-A failure.
4. BGP convergence.
5. ISP-B becomes the available path.
6. ISP-A restoration.
7. Normal path preference returns.

---

### OSPF and BGP Boundary

OSPF and BGP will have clearly defined responsibilities.

OSPF will carry routes within the Meridian enterprise.

BGP will carry routes between Meridian and external Internet service
providers.

The edge routers will provide the boundary between the internal OSPF domain
and external BGP routing.

Route redistribution between OSPF and BGP will be minimized and performed
only where required.

---

### HSRP

HSRP will provide redundant default gateways for critical internal VLANs.

The Layer 3 devices will advertise a shared virtual gateway address to
clients.

Under normal conditions:

    Core-1
      |
    HSRP Active
      |
    Virtual Gateway
      |
    Clients

If Core-1 fails:

    Core-2
      |
    HSRP Active
      |
    Virtual Gateway
      |
    Clients

HSRP will provide gateway redundancy while OSPF provides routing between
Layer 3 network devices.

---

### IPv6 Routing

IPv6 will use OSPFv3 as the internal IPv6 routing protocol.

The IPv6 design will follow the same general hierarchical architecture as
the IPv4 routing design.

The project will demonstrate:

- IPv6 addressing
- OSPFv3 neighbor relationships
- IPv6 route exchange
- IPv6 path selection
- IPv6 failover

---

### Routing Verification

Routing behavior will be validated using operational commands and controlled
failure testing.

The following commands will be used during validation:

    show ip route
    show ip ospf neighbor
    show ip ospf interface
    show ip protocols
    show ip bgp summary
    show ip bgp
    show ip route bgp
    show standby brief
    show ipv6 route
    show ipv6 ospf neighbor

Packet captures will also be used where appropriate to analyze routing
protocol behavior.

---

### Routing Failure Testing

The following failures will be intentionally introduced:

- OSPF neighbor/link failure
- Primary WAN path failure
- ISP-A failure
- HSRP active-router failure
- Secondary-path recovery
- BGP neighbor failure

Each failure will be documented with:

- Initial state
- Failure introduced
- Routing-protocol state
- Routing-table changes
- Traffic behavior
- Recovery
- Final state

## 7. Security Architecture

The Meridian Financial Services network will use a layered security
architecture to protect corporate users, servers, management systems, and
Internet-facing services.

Security controls will be implemented at multiple layers, including network
segmentation, firewalls, identity-based access control, VPN encryption,
centralized authentication, and centralized logging.

### Security Zones

The network will be divided into logical security zones based on the
sensitivity and purpose of the systems within each zone.

The primary security zones will be:

| Zone | Purpose |
|---|---|
| OUTSIDE | Untrusted Internet traffic |
| INSIDE | Corporate user networks |
| SERVER | Internal application and server networks |
| DMZ | Public-facing services |
| GUEST | Guest and Internet-only access |
| MANAGEMENT | Network and infrastructure management |
| VPN | Remote-access and site-to-site VPN traffic |

Traffic between security zones will be controlled according to business and
security requirements.

---

### Firewall Architecture

Firewalls will provide the primary security boundary between the Internet
and the internal corporate network.

The high-level traffic path will be:

    Internet
       |
    ISP-A / ISP-B
       |
    Edge Routers
       |
    Firewall
       |
    Internal Network

The firewall will provide:

- Stateful traffic inspection
- Security policies
- Network Address Translation (NAT)
- Internet access control
- DMZ protection
- VPN termination
- Logging of security events

Where practical, redundant firewalls will be used at critical locations to
reduce the impact of a firewall failure.

---

### Network Segmentation

Internal networks will be separated into VLANs based on function.

The initial segmentation will include:

| VLAN | Purpose |
|---|---|
| 10 | Corporate Users |
| 20 | Voice |
| 30 | Servers |
| 40 | Guest |
| 50 | Management |
| 60 | Printers/IoT |
| 70 | Network Infrastructure |

Segmentation will reduce unnecessary communication between network groups and
limit the potential impact of compromised devices.

---

### Guest Network Security

Guest devices will be isolated from internal corporate resources.

Guest users will be permitted to access the Internet but will not be
permitted to access:

- Corporate user networks
- Server networks
- Management networks
- Network infrastructure
- Internal applications

The guest network will use separate VLAN and security policies.

---

### Server Network Security

Critical servers will be placed in a dedicated server network.

Access to server resources will be restricted based on the required
application and business function.

Users will not receive unrestricted access to the server network.

Firewall or Layer 3 security policies will restrict access to only required
services and protocols.

---

### Management Network Security

Network infrastructure will use a dedicated management network.

Management access will be restricted to authorized administrators and
management systems.

Administrative access will use secure protocols such as SSH and HTTPS.

Telnet and other insecure management protocols will not be used.

---

### Identity and Access Control

Cisco ISE will provide centralized identity-based access control for
supported network-access scenarios.

ISE will be used for:

- 802.1X authentication
- RADIUS authentication and authorization
- Network access policies
- VLAN assignment
- Device authorization
- Guest access policies

Network access decisions will be based on user and device identity where
appropriate.

---

### Network Device Administration

Network-device administrative access will use centralized AAA.

TACACS+ will be used for administrative authentication and authorization of
supported network devices.

The design will provide:

- Centralized administrator authentication
- Authorization of administrative actions
- Accounting of administrative sessions
- Local authentication fallback for emergency access

---

### Site-to-Site VPN Security

IPsec VPNs will provide encrypted connectivity between corporate locations
when traffic traverses an untrusted or public network.

The VPN design will provide:

- Encrypted site-to-site communication
- Strong authentication
- Confidentiality
- Integrity protection
- Controlled encryption domains

The IPsec VPN will also serve as the backup WAN path for branch connectivity.

---

### Remote-Access VPN Security

Remote employees will use an encrypted remote-access VPN to access approved
corporate applications.

Remote VPN access will require authentication and authorization.

Remote users will not receive unrestricted access to the entire corporate
network.

Access will be limited to approved applications and resources based on
security policy.

---

### DMZ Security

Public-facing services that must be reachable from the Internet will be
placed in a DMZ rather than directly on the internal corporate network.

The DMZ will provide an additional security boundary between public-facing
services and internal systems.

The expected traffic model is:

    Internet
       |
    Firewall
       |
      DMZ
       |
    Firewall
       |
    Internal Network

Internet users will not be permitted to directly access internal corporate
networks.

---

### Security Logging

Security-relevant events will be forwarded to centralized logging and SIEM
systems.

Events will include:

- Firewall denies
- VPN authentication events
- Failed administrator logins
- Successful administrator logins
- ISE authentication events
- Network-device security events
- Configuration changes where supported

Centralized logging will provide visibility for security investigations and
incident response.

---

### Security Monitoring

Security infrastructure will be monitored for availability and abnormal
conditions.

Monitoring will include:

- Firewall availability
- VPN status
- Authentication failures
- Interface failures
- Excessive traffic
- Device availability
- Security-policy events

Alerts will be generated for important security and infrastructure events.

---

### Security Failure Testing

The project will include controlled security failures to validate the
design.

Examples include:

- Incorrect firewall policy
- Failed VPN authentication
- Failed ISE authentication
- Unauthorized VLAN access attempt
- Guest-to-server access attempt
- Failed administrator authentication

Each security incident will be documented with the observed symptoms,
evidence, root cause, remediation, and validation.

---

### Security Design Goals

The security architecture will:

- Protect internal resources from untrusted networks.
- Restrict communication between security zones.
- Provide identity-based network access.
- Secure remote and site-to-site connectivity.
- Protect public-facing services using a DMZ.
- Secure network-device administration.
- Provide centralized security logging.
- Provide sufficient visibility to investigate security incidents.

## 8. Data Center / DR Architecture

The Ashburn, Virginia facility will serve as the primary disaster recovery
(DR) and data center location for Meridian Financial Services.

The DR architecture will provide a secondary location for critical network
and business services if the New York headquarters becomes unavailable.

### DR Objectives

The DR site will:

- Provide access to critical applications during a major HQ failure.
- Provide redundant connectivity to the corporate network.
- Maintain critical authentication and infrastructure services.
- Provide centralized monitoring and logging capabilities.
- Support recovery of critical business services.
- Minimize disruption to users during a major site failure.

### Data Center Network Architecture

The Ashburn facility will use a redundant Layer 3 network design.

The high-level architecture will include:

- Redundant core/distribution devices
- Server networks
- Management network
- Security infrastructure
- WAN connectivity
- Internet connectivity where required
- Monitoring and logging infrastructure

The data center network will participate in the enterprise OSPF routing
domain.

### Critical Services

The following services will be considered critical for disaster recovery:

| Service | Purpose |
|---|---|
| DNS | Name resolution |
| DHCP | Client network configuration |
| Authentication | User and infrastructure authentication |
| Network Management | Monitoring and management |
| SIEM/Logging | Security and operational logging |
| Internal Applications | Critical business applications |
| Backup Services | Data and configuration recovery |

Critical services will be designed so that they can continue operating or be
restored at the DR site if the primary environment becomes unavailable.

### HQ-to-DR Connectivity

New York HQ and Ashburn will have redundant connectivity.

The primary path will use the enterprise WAN.

A secondary path will use an encrypted IPsec VPN over an available Internet
connection.

Normal operation:

    New York
       |
       | Primary WAN
       |
    Ashburn

If the primary path fails:

    New York
       |
       X Primary WAN
       |
       | IPsec VPN
       |
    Ashburn

OSPF will provide dynamic route selection and allow traffic to use the
available backup path.

### DR Routing

Ashburn will participate in the enterprise OSPF topology.

The DR site will advertise its internal networks through OSPF and learn
required corporate routes from the enterprise routing domain.

Route summarization will be used where appropriate to reduce unnecessary
routing information.

### DR Security

Critical DR services will be protected using the same security principles as
the primary environment.

The DR environment will include:

- Firewall protection
- Network segmentation
- Dedicated management networks
- Restricted administrative access
- Centralized authentication
- VPN security
- Centralized logging

Critical servers will not be directly exposed to the Internet.

### DR Server Segmentation

Servers will be separated from user and management networks.

The high-level segmentation will include:

- Server network
- Management network
- Backup network where appropriate
- DMZ where public-facing services are required

Access between these networks will be controlled by appropriate security
policies.

### Backup and Recovery

Network configurations and critical system data will be backed up to
appropriate storage at the DR site.

The project will demonstrate recovery of selected critical services rather
than attempting to replicate the entire production environment.

Network-device configurations will also be backed up so that infrastructure
can be restored after a major failure.

### Disaster Recovery Scenario

The primary DR scenario will simulate a complete loss of the New York
environment.

The test will include:

1. Simulate loss of the primary HQ network.
2. Verify that the Ashburn facility remains reachable.
3. Verify that critical services remain available or can be restored.
4. Verify that routing converges toward the DR environment.
5. Verify remote and branch connectivity.
6. Verify monitoring and logging remain operational.
7. Restore the primary environment.
8. Verify normal routing and service operation.

### Recovery Target

Critical network and business services should be recoverable at the Ashburn
DR site within four hours following a major HQ failure.

The project will document the recovery process and identify any services that
require manual intervention.

### DR Monitoring

The DR environment will be monitored using the centralized monitoring and
logging infrastructure.

Monitoring will include:

- Device availability
- WAN connectivity
- Server availability
- Interface utilization
- CPU and memory
- Routing-protocol status
- VPN status
- Security events
- Backup status

### DR Design Goals

The DR architecture will:

- Provide a secondary location for critical services.
- Maintain connectivity during a primary-site failure.
- Provide secure connectivity between HQ and DR.
- Minimize single points of failure.
- Support recovery of critical services within the defined recovery target.
- Provide centralized monitoring and logging.

## 9. High Availability

Meridian Financial Services will use redundant network paths, devices, and
services where appropriate to minimize service disruption caused by individual
failures.

The high-availability design will focus on eliminating critical single points
of failure and providing automatic or rapid recovery when a component fails.

### High Availability Goals

The network should:

- Maintain connectivity during a single device failure where practical.
- Maintain connectivity during a single WAN-path failure.
- Maintain Internet access during a single ISP failure.
- Maintain LAN gateway availability during a core-device failure.
- Maintain connectivity during individual link failures.
- Provide recovery capabilities if the primary HQ environment becomes
  unavailable.

---

### Internet Redundancy

New York HQ will use two independent Internet service providers.

The Internet edge will consist of redundant edge routers with BGP sessions to
the providers.

Normal operation:

    ISP-A
      |
    Edge-R1
      |
    Firewall
      |
    Enterprise

If ISP-A fails:

    ISP-A X

    ISP-B
      |
    Edge-R2
      |
    Firewall
      |
    Enterprise

BGP will allow the network to select the available ISP path.

---

### WAN Path Redundancy

Each branch will have a primary WAN path and a secondary IPsec VPN path.

The primary WAN path will be preferred during normal operation.

The IPsec VPN will provide a backup path over an available Internet
connection.

Normal operation:

    Branch
       |
       | Primary WAN
       |
       v
      HQ

After primary WAN failure:

    Branch
       |
       X Primary WAN
       |
       | IPsec VPN
       |
       v
      HQ

OSPF will dynamically select the available path.

The primary WAN path will have a lower OSPF cost than the backup path.

---

### Core Device Redundancy

Critical sites will use redundant Layer 3 devices to reduce the impact of a
single core-device failure.

HSRP will provide a shared virtual default gateway for internal VLANs.

Normal operation:

    Core-1
      |
    HSRP Active
      |
    Virtual Gateway
      |
    Clients

After Core-1 failure:

    Core-1 X

    Core-2
      |
    HSRP Active
      |
    Virtual Gateway
      |
    Clients

Clients will continue using the same virtual gateway address.

---

### Link Redundancy

Critical switch-to-switch connections will use multiple physical links
bundled with LACP.

Normal operation:

    Switch A
      || 
      || LACP
      ||
    Switch B

If one physical link fails:

    Switch A
      |X
      || LACP
      ||
    Switch B

The remaining links will continue carrying traffic.

---

### Spanning Tree Redundancy

Spanning Tree Protocol will prevent Layer 2 loops while maintaining
redundant physical paths.

The STP design will establish predictable root placement.

If an active Layer 2 path fails, STP will allow an available redundant path
to become active.

---

### Firewall Redundancy

Where supported by the selected firewall platform, redundant firewalls will
be deployed at critical locations.

The firewall design will provide a mechanism for maintaining network
connectivity if the active firewall becomes unavailable.

Firewall redundancy will be validated through controlled failure testing.

---

### Routing Convergence

Dynamic routing protocols will provide automatic recovery from routing and
WAN failures.

OSPF will provide internal route convergence.

BGP will provide external route convergence and ISP failover.

Routing convergence will be validated by intentionally failing links and
devices and observing changes in:

- Routing tables
- OSPF neighbor relationships
- BGP neighbor relationships
- Traffic paths
- Monitoring alerts

---

### Data Center Redundancy

The Ashburn DR/Data Center will provide an alternate location for critical
services.

Critical services will have recovery capabilities at Ashburn in the event
of a major New York failure.

The DR environment will use redundant network connectivity where practical.

---

### Failure Scenarios

The following failure scenarios will be tested:

#### ISP Failure

    ISP-A X
       |
       v
    BGP convergence
       |
       v
    ISP-B

Expected result:

Internet connectivity remains available through ISP-B.

#### Primary WAN Failure

    Primary WAN X
         |
         v
    OSPF convergence
         |
         v
    IPsec backup

Expected result:

The branch maintains connectivity to critical corporate resources.

#### Core Router Failure

    Core-1 X
       |
       v
    HSRP
       |
       v
    Core-2

Expected result:

Clients retain their default gateway through the HSRP virtual IP.

#### Physical Link Failure

    LACP member X
          |
          v
    Remaining LACP members

Expected result:

Connectivity remains available through the remaining physical links.

#### HQ Failure

    New York HQ X
           |
           v
      Ashburn DR
           |
           v
    Critical services

Expected result:

Critical services can be recovered or remain available through the DR
environment.

---

### High Availability Validation

Each redundancy mechanism will be validated using controlled failure tests.

For each test, the following information will be documented:

1. Initial network state.
2. Failure introduced.
3. Detection mechanism.
4. Routing or redundancy protocol response.
5. Traffic behavior.
6. Service impact.
7. Recovery time.
8. Restoration of the failed component.
9. Final network state.

Evidence will include CLI output, monitoring alerts, routing tables, packet
captures, and connectivity tests where appropriate.

---

### High Availability Design Summary

The network will use multiple layers of redundancy:

| Component | Redundancy Mechanism |
|---|---|
| Internet | Dual ISPs |
| Internet routing | BGP |
| WAN | Primary WAN + IPsec backup |
| Internal routing | OSPF |
| Default gateway | HSRP |
| Switch links | LACP |
| Layer 2 paths | STP |
| Firewalls | Firewall HA where supported |
| Critical services | Ashburn DR |
| Monitoring/logging | Centralized infrastructure |

The goal is not to eliminate every possible failure, but to ensure that a
single failure does not unnecessarily cause a major service outage.

## 10. Management and Monitoring

Meridian Financial Services will use centralized management, monitoring,
logging, and documentation to provide operational visibility across the
enterprise network.

The management architecture will allow network administrators to identify
failures, investigate performance problems, review security events, maintain
accurate network documentation, and back up device configurations.

### Network Documentation

NetBox will serve as the primary network source of truth.

NetBox will maintain information about:

- Sites
- Devices
- Device roles
- Interfaces
- IP addresses
- Prefixes
- VLANs
- VRFs
- WAN circuits
- Device connections

Network documentation will be maintained as the network changes.

The physical and logical topology documented in NetBox should remain
consistent with the deployed network.

---

### Network Monitoring

SolarWinds will provide centralized infrastructure monitoring.

The monitoring platform will monitor:

- Routers
- Switches
- Firewalls
- WAN links
- Interfaces
- Device availability
- CPU utilization
- Memory utilization
- Interface utilization
- Packet loss
- Latency
- Interface errors

Monitoring will allow administrators to detect infrastructure failures and
performance problems before they become larger outages.

---

### Network Alerts

Monitoring alerts will be configured for important operational events.

Examples include:

- Device unavailable
- Interface down
- High interface utilization
- High CPU utilization
- High memory utilization
- Excessive packet loss
- High latency
- OSPF neighbor failure
- BGP neighbor failure
- VPN failure

Alerts will be designed to identify events that require administrator
attention rather than generating unnecessary notifications.

---

### SNMP

SNMP will be used to provide network-management information to the
centralized monitoring platform.

Where supported, SNMPv3 will be preferred because it provides authentication
and encryption.

SNMP will be used to collect information such as:

- Interface status
- Interface traffic
- Device health
- CPU utilization
- Memory utilization
- Hardware information

SNMP access will be restricted to authorized monitoring systems.

---

### Syslog

Network devices and security infrastructure will send system and security
events to a centralized syslog/SIEM platform.

Events may include:

- Interface state changes
- Authentication events
- Configuration changes
- Routing events
- VPN events
- Firewall events
- Security events

Centralized logging will allow administrators to correlate events across
multiple devices.

---

### SIEM

The SIEM platform will provide centralized analysis of security and
operational events.

The SIEM will receive logs from:

- Routers
- Switches
- Firewalls
- ISE
- VPN infrastructure
- Servers
- Other critical network systems

The project will use the SIEM to investigate security and infrastructure
events.

Example searches will include:

- Failed authentication attempts
- Successful administrator logins
- Firewall denies
- VPN authentication failures
- OSPF events
- BGP events
- Device configuration changes

---

### NTP

Network devices and management systems will use Network Time Protocol (NTP)
to maintain consistent system time.

Accurate time synchronization is required for:

- Syslog correlation
- SIEM analysis
- Authentication
- Troubleshooting
- Incident investigation
- Configuration auditing

All critical network infrastructure should use a consistent time source.

---

### Configuration Backups

Network-device configurations will be backed up regularly.

Backups will include:

- Router configurations
- Switch configurations
- Firewall configurations
- Other critical network infrastructure

Configuration backups will allow administrators to restore devices after
configuration errors or device failures.

Backups will be stored separately from the devices being backed up.

---

### Network Automation

The network will be designed to support automation using NetBox, Python,
Jinja2, and Ansible.

NetBox will provide structured network information that can be consumed by
automation tools.

The planned automation workflow is:

    NetBox
       |
       v
    Python / Ansible
       |
       v
    Jinja2 Templates
       |
       v
    Network Devices

Automation will initially focus on repeatable tasks such as:

- Configuration generation
- VLAN configuration
- Interface configuration
- Device configuration backups
- Configuration validation
- Operational data collection

Automation will be introduced after the manual network design has been
validated.

---

### Management Network

Management traffic will use a dedicated management network.

Only authorized management systems and administrators will be permitted to
access network-device management interfaces.

Management access will use secure protocols such as:

- SSH
- HTTPS
- SNMPv3
- TACACS+

Telnet will not be used for administrative access.

---

### Monitoring During Incidents

Monitoring and logging will be used as part of the incident-response
process.

For example:

    Device Failure
         |
         v
    SolarWinds Alert
         |
         v
    Administrator Investigation
         |
         +----> Routing Tables
         |
         +----> Device Logs
         |
         +----> SIEM
         |
         +----> Wireshark
         |
         v
      Root Cause
         |
         v
        Fix
         |
         v
      Validation

The project will include controlled failures to demonstrate this workflow.

---

### Management and Monitoring Validation

The following capabilities will be tested:

- Device discovery and monitoring
- SNMP polling
- Syslog collection
- NTP synchronization
- Monitoring alerts
- BGP/OSPF monitoring
- VPN monitoring
- Configuration backups
- Centralized authentication
- SIEM event collection
- NetBox documentation accuracy

Each system will be validated independently before being used as part of
the final incident-response demonstrations.

---

### Management and Monitoring Design Goals

The management architecture will provide:

- Accurate network documentation
- Centralized infrastructure monitoring
- Centralized event logging
- Security-event visibility
- Consistent time synchronization
- Configuration recovery
- Secure administrative access
- Automation readiness
- Operational visibility during network failures

### 11. High-Level Topology


The following diagram represents the high-level architecture of the
Meridian Financial Services enterprise network.

![High-Level Enterprise Topology](../diagrams/enterprise-high-level.png)
