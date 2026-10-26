# Network Incident Response Lab

A PNETLab-based set of nine network incidents, each documented as a realistic root cause analysis (RCA) case with the evidence an employer can review.

Part of my networking portfolio: [richardpateau.github.io](https://richardpateau.github.io) | [Networking Notebook (blog)](https://networkingnotebook.com/) | [Enterprise Network Design](https://github.com/richardpateau/enterprise-network-design)

## Workflow

Every incident follows the same path:

**Ticket → Symptoms → Investigation → Evidence → Root Cause → Fix → Verification → Close**

## Purpose

This project shows how I approach network troubleshooting in an operations environment, not just that I can build a topology.

The incidents are ordered roughly by increasing complexity. They start with a straightforward Layer 2/3 service failure and build toward protocol-internals problems (OSPF DBD/MTU, BGP prefix advertisement, HSRP redundancy logic), where the fix requires understanding why the protocol behaves the way it does, not just which command to run.

Each case produces:

- a ticket
- CLI output
- packet captures
- monitoring screenshots
- before/after configs
- a written root-cause analysis

## Lab Environment

A small enterprise-style network built in PNETLab and reused across incidents:

- Access LAN and clients
- Edge routing
- Internal application network
- WAN / ISP connectivity
- Centralized logging and SNMP monitoring

![Lab topology](docs/lab-topology.png)

Each incident folder also contains the topology used for that specific case.

**Platform and tools:** PNETLab, Cisco CSR1000v / IOSvL2, Wireshark / tcpdump, Splunk, SolarWinds NPM, ServiceNow-style ticketing.

## Incidents

| Incident | Symptom | Root cause | Skills shown |
|---|---|---|---|
| [INC-001](incidents/INC-001-DHCP-Failure/) | Clients cannot obtain an IP address | DHCP pool and default-router set for `10.10.20.0/24` while the LAN is `10.10.10.0/24` | DHCP, DORA, Wireshark, config mismatch |
| [INC-002](incidents/INC-002-OSPF-Adjacency-Failure/) | Remote LAN unreachable, but R1 can ping R2 | Shared transit link configured in different OSPF areas, so the adjacency never reached FULL | OSPF states, routing table, packet analysis |
| [INC-003](incidents/INC-003-ACL-Traffic-Blocked/) | Change meant to block Telnet also broke ping and HTTPS | Over-broad `deny ip`, then a leftover deny for TCP/443 | Extended ACLs, hit counters, two-stage RCA |
| [INC-004](incidents/INC-004-OSPF-MTU-Mismatch/) | OSPF neighbor stuck in EXSTART, remote route missing | Interface MTU mismatch stalled the DBD exchange; fixed by matching MTU, not `ip ospf mtu-ignore` | MTU, DBD exchange, adjacency state machine |
| [INC-005](incidents/INC-005-SNMP-Monitoring-Failure/) | SolarWinds shows R1 down, but ping and SSH work | SNMPv2c community typo (`NOC-R0` vs `NOC-RO`) | SNMP, SolarWinds, UDP/161, layered checks |
| [INC-006](incidents/INC-006-DHCP-Relay-Failure/) | Clients fail to get addresses from a remote DHCP server | `ip helper-address` pointed at `10.20.20.11` instead of `10.20.20.1` | DHCP relay, helper-address, centralized DHCP |
| [INC-007](incidents/INC-007-NAT-Translation-Failure/) | Internal traffic works, public hosts unreachable | NAT ACL matched `10.10.20.0/30` instead of the user LAN `10.10.10.0/24` | NAT/PAT, NAT ACL, translation table |
| [INC-008](incidents/INC-008-BGP-Route-Advertisement-Failure/) | eBGP session Established, but the ISP has no route to the LAN | `network 10.10.100.0` did not match the `10.10.10.0/24` prefix in the routing table | eBGP, network statement, advertised-routes |
| [INC-009](incidents/INC-009-HSRP-Failover-Failure/) | Gateway stops responding when the primary router fails | R2 configured with standby VIP `10.10.10.11` instead of `10.10.10.1` | HSRP, VIP mismatch, ARP, failover testing |

## How Each Incident Is Structured

```
INC-00X-Name/
├── README.md
├── topology/
└── evidence/
    ├── configs/
    ├── pcaps/
    └── screenshots/
```

Every incident README includes: Ticket, Expected state, Symptoms, Investigation evidence, Root cause, Resolution, Verification, and Lessons learned.

## Tools and Methods

**CLI:** Cisco routing, switching, DHCP, NAT, BGP, HSRP, ACL, and SNMP verification.

**Packet analysis:** DHCP DORA, OSPF Hello/DBD, ACL drops, SNMP polling, NAT translation, HSRP/ARP failover.

**Monitoring:** SolarWinds for device, interface, and routing neighbor status. Splunk for syslog correlation. Cases where monitoring showed nothing are documented as well.

**Ticketing:** ServiceNow-style intake and resolution notes.

## Where to Start

If you only have a few minutes, these five show the most depth:

- [INC-003 ACL](incidents/INC-003-ACL-Traffic-Blocked/): a two-stage fix, where the first change hid a second fault
- [INC-004 OSPF MTU](incidents/INC-004-OSPF-MTU-Mismatch/): the link and Hellos were fine; the failure was inside the DBD exchange
- [INC-007 NAT](incidents/INC-007-NAT-Translation-Failure/): proven with translation tables and before/after captures
- [INC-008 BGP](incidents/INC-008-BGP-Route-Advertisement-Failure/): the session was healthy, but the wrong prefix was configured
- [INC-009 HSRP](incidents/INC-009-HSRP-Failover-Failure/): failover tested with the primary still down

## Notes

- This is a lab environment, not a production network.
- Faults were injected so the troubleshooting process could be documented end to end.
- Monitoring gaps are included on purpose when SolarWinds or Splunk did not generate useful alerts.

## Related

- [Portfolio site](https://richardpateau.github.io)
- [Enterprise Network Design](https://github.com/richardpateau/enterprise-network-design): the larger multi-site design project
- [Networking Notebook](https://networkingnotebook.com/): technical writing on the protocols used in these labs
