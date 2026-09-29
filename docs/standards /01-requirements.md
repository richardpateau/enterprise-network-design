# Meridian Financial Services
## Network Requirements

## 1. Company Profile

- **Industry:** Financial Services
- **Headquarters:** New York, NY
- **Employees:** Approximately 1,200
- **Corporate Sites:** 4
- **Disaster Recovery Site:** Ashburn, VA

### Site Distribution

| Site | Location | Users | Purpose |
|---|---|---:|---|
| HQ | New York, NY | 500 | Corporate headquarters |
| Branch 1 | Chicago, IL | 300 | Regional office |
| Branch 2 | Dallas, TX | 200 | Regional office |
| Branch 3 | Miami, FL | 200 | Regional office |
| DR/Data Center | Ashburn, VA | Infrastructure only | Disaster recovery and critical services |

**Total employee population:** Approximately 1,200 users.

---

## 2. Business Requirements

### User Capacity

The network must support approximately 1,200 users initially and provide sufficient capacity for future growth toward 2,000 users.

### Multi-Site Connectivity

All corporate sites must have reliable connectivity to HQ, the DR/Data Center, and required corporate applications.

### Internet Access

Employees and business systems require reliable Internet access for business applications, cloud services, email, collaboration, and general corporate use.

### Secure Remote Access

Remote employees must be able to securely access approved corporate applications and resources through a remote-access VPN.

### Site-to-Site Connectivity

Corporate sites must securely communicate with HQ and the DR/Data Center using encrypted site-to-site connectivity.

### High Availability

Critical network services should remain available during individual device, link, or provider failures where practical.

### Centralized Authentication

Network access and network-device administration must support centralized authentication and authorization.

### Network Monitoring

Network infrastructure must be monitored for availability, performance, utilization, and failures.

### Centralized Logging

Network, security, authentication, VPN, and infrastructure events must be collected in a centralized logging/SIEM platform.

### IP Address Documentation

IP addresses, prefixes, VLANs, interfaces, devices, sites, and WAN circuits must be centrally documented and maintained in NetBox.

### Disaster Recovery

Critical services must be recoverable at the Ashburn DR/Data Center if the primary environment becomes unavailable.

---

## 3. Measurable Requirements

- HQ must have **dual ISP connections** for Internet redundancy.
- Each branch must remain connected to critical corporate resources if **one WAN path fails**.
- Guest traffic must be **isolated from internal server and corporate networks**.
- Remote VPN users must be restricted to **approved applications and resources**.
- Critical network services should be restored at the DR site within **4 hours** following a major site failure.
- Network infrastructure must provide **centralized monitoring and logging** for operational and security events.

---

## 4. Security Requirements

The network must provide:

- Network segmentation
- Identity-based access control
- Secure administrative access
- Firewall protection
- Site-to-site IPsec VPN
- Remote-access VPN
- Centralized authentication
- Centralized logging
- Guest network isolation
- Restricted management access

---

## 5. Availability Requirements

The network should minimize single points of failure for critical services.

The design will use appropriate redundancy for:

- Internet connectivity
- Core routing
- Default gateways
- WAN connectivity
- Critical security infrastructure

---

## 6. Critical Applications

Meridian relies on:

- Financial applications
- Internal business applications
- Microsoft 365
- Email
- Voice and video conferencing
- DNS
- DHCP
- Authentication services
- Network monitoring
- SIEM/logging

---

## 7. Disaster Recovery

The Ashburn, Virginia facility will serve as the organization's disaster recovery and data center location.

Critical infrastructure and services will have a recovery capability at the DR site in the event that the primary environment becomes unavailable.

---

## 8. Out of Scope — Phase 1

The following technologies are intentionally excluded from the initial project scope:

- SD-WAN
- VXLAN/EVPN
- Cloud networking
- Wireless controller deployment
- Advanced application delivery/load balancing

These technologies may be considered in future project phases.

---

## 9. Project Success Criteria

Success means users can reach corporate applications and the Internet, sites stay connected during a single WAN or ISP failure, and the network is documented in NetBox with monitoring and centralized logging in place.
