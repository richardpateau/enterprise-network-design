# Azure Architecture – Meridian Financial Services
 
Baseline hybrid architecture connecting the Meridian on-premises network to Azure via a route-based site-to-site IKEv2/IPsec VPN.
 
---
 
## 1. Purpose
 
This document describes the high-level Azure architecture for Meridian Financial Services, including:
 
- Virtual network design and addressing
- Hybrid connectivity to the on-premises Meridian network
- Private application workloads
- Controlled Internet egress
- Core security and design principles
Detailed implementation, testing, and evidence live in the related folders listed at the end.
 
---
 
## 2. High-Level Topology

![Topology](evidence/screenshots/high-level-diagram.png)
 
---
 
## 3. Azure Resource Group
 
| Component       | Value                |
|-----------------|----------------------|
| Resource Group  | Meridian-Azure-RG    |
| Region          | East US              |
 
**Screenshot – Azure Resource Group**  
`screenshots/azure-resource-group.png`  
*(Resource group overview showing core resources)*
 
---
 
## 4. Virtual Network
 
| Component      | Configuration              |
|----------------|----------------------------|
| VNet           | Meridian-Azure-VNet        |
| Address Space  | 10.200.0.0/16              |
| Region         | East US                    |
| Resource Group | Meridian-Azure-RG          |
 
**Screenshot – VNet and address space**  
`screenshots/vnet-address-space.png`  
*(VNet overview with address space 10.200.0.0/16)*
 
---
 
## 5. Subnet Layout
 
| Subnet                | Address Space     | Purpose                        |
|-----------------------|-------------------|--------------------------------|
| Azure-Apps            | 10.200.10.0/24    | Application workloads          |
| Azure-Infrastructure  | 10.200.20.0/24    | Infrastructure workloads       |
| GatewaySubnet         | 10.200.255.0/27   | Azure VPN Gateway              |
 
**Screenshot – Subnet layout**  
`screenshots/subnet-layout.png`  
*(Subnet list showing Azure-Apps, Azure-Infrastructure, and GatewaySubnet)*
 
---
 
## 6. Hybrid Connectivity
 
Meridian connects its on-premises network to Azure using a **route-based site-to-site IPsec VPN**.
 
### Azure VPN Gateway
 
| Component     | Configuration                          |
|---------------|----------------------------------------|
| Name          | Microsoft-Azure-VGW                    |
| Region        | East US                                |
| SKU           | VpnGw2AZ                               |
| Type          | Route-based                            |
| Active-Active | Enabled                                |
| BGP           | Disabled                               |
| IKE Version   | IKEv2                                  |
 
The Azure VPN Gateway terminates the encrypted connection to the Meridian ASA HA pair.
 
On-premises side:
- Primary firewall uses a route-based IPsec VTI (`Tunnel100`, 172.31.254.1/30)
- Existing Meridian site-to-site VPN architecture remains separate from the Azure VPN
**Screenshot – VPN Gateway**  
`screenshots/vpn-gateway.png`  
*(VPN Gateway overview / connection status)*
 
---
 
## 7. Azure Application Workload
 
| Attribute        | Value                          |
|------------------|--------------------------------|
| Hostname         | MERIDIAN-AZ-WEB01              |
| Operating System | Ubuntu Server 24.04 LTS        |
| Private IP       | 10.200.10.4                    |
| Subnet           | Azure-Apps (10.200.10.0/24)    |
| Web Server       | Apache HTTP Server             |
| Public IP        | None                           |
 
The VM hosts a custom Meridian Financial Services webpage and is intentionally deployed **without a public IP**. Access is intended only from the Meridian network over the site-to-site VPN.
 
**Screenshot – Azure VM placement**  
`screenshots/azure-vm-placement.png`  
*(VM overview showing private IP, subnet, and no public IP)*
 
---
 
## 8. Internet Egress
 
Outbound Internet access for Azure application workloads is provided through an **Azure NAT Gateway**.
 
```text
MERIDIAN-AZ-WEB01 (10.200.10.4)
        |
        v
   Azure-Apps
        |
        v
   NAT Gateway
        |
        v
    Internet
```
 
This enables package updates, software installation, and outbound application traffic while keeping the VM privately addressed and not directly Internet-reachable.
 
**Screenshot – NAT Gateway relationship**  
`screenshots/nat-gateway-relationship.png`  
*(NAT Gateway associated with Azure-Apps subnet / outbound connectivity path)*
 
---
 
## 9. Security Architecture (Summary)
 
- Application subnet controlled by Network Security Group
- Web server privately accessible from Meridian network (10.0.0.0/8 → TCP/80 allowed initially)
- No public IP on the application server
- Layered controls: NSG + on-premises firewall + private addressing + encrypted VPN
Further hardening and rule review are documented in `06-Security/`.
 
---
 
## 10. Traffic Flows
 
### Meridian → Azure Application
 
```text
Meridian Client → Meridian LAN → HQ Firewall
        → IKEv2/IPsec → Azure VPN Gateway
        → Azure VNet → Azure-Apps → 10.200.10.4 (Apache)
```
 
### Azure → Internet
 
```text
10.200.10.4 → Azure-Apps → NAT Gateway → Internet
```
 
### Azure → Meridian
Azure resources reach Meridian on-premises networks via the site-to-site VPN (routes as configured).
 
---
 
## 11. Design Principles
 
- **Private application workloads** – No public IPs on application servers  
- **Hybrid connectivity** – Encrypted site-to-site IPsec to Meridian  
- **Network segmentation** – Separate Apps and Infrastructure subnets  
- **Controlled Internet egress** – NAT Gateway instead of direct public addressing  
- **Layered security** – NSG, firewall, private addressing, VPN  
- **Documented validation** – Packet captures, CLI, connectivity, and application tests  
---
 
## 12. Current Implementation Status
 
### Completed
- Azure subscription and resource group  
- Azure VNet and subnets (Apps, Infrastructure, Gateway)  
- Azure VPN Gateway + Local Network Gateway + site-to-site connection  
- IKEv2 negotiation and ASA route-based VTI  
- VPN connectivity testing  
- Application VM (private addressing) + Apache + Meridian webpage  
- NAT Gateway and controlled outbound Internet  
### Planned
- Complete application-layer VPN testing  
- Azure security hardening  
- Azure routing documentation  
- Monitoring / Log Analytics  
- Backup and disaster recovery  
- VPN failover testing  
- Additional workloads as required  
- Final architecture validation  
---
 
## 13. Screenshots (Architecture Support Only)
 
Place supporting screenshots in `screenshots/` (or link from `diagrams/` where appropriate):
 
| Screenshot                        | File (suggested)                     | Purpose                                      |
|-----------------------------------|--------------------------------------|----------------------------------------------|
| High-level Azure topology         | `high-level-azure-topology.png`      | Overall design                               |
| Azure Resource Group              | `azure-resource-group.png`           | Resource group overview                      |
| VNet and address space            | `vnet-address-space.png`             | 10.200.0.0/16                                |
| Subnet layout                     | `subnet-layout.png`                  | Apps / Infrastructure / GatewaySubnet        |
| VPN Gateway                       | `vpn-gateway.png`                    | Gateway and hybrid connection                |
| Azure VM placement                | `azure-vm-placement.png`             | MERIDIAN-AZ-WEB01 private placement          |
| NAT Gateway relationship          | `nat-gateway-relationship.png`       | Outbound Internet path                       |
 
Only screenshots that illustrate the overall architecture are kept here. Implementation detail, packet captures, and test evidence belong in the respective folders (`03-Site-to-Site-VPN`, `04-Application-Server`, `10-Testing`, `11-Evidence`, etc.).
 
---
 
## 14. Related Documentation
 
| Folder / Doc                  | Contents                                      |
|-------------------------------|-----------------------------------------------|
| `02-Networking/`              | VNet and subnet configuration                 |
| `03-Site-to-Site-VPN/`        | Azure VPN and ASA IPsec implementation        |
| `04-Application-Server/`      | Azure VM and Apache configuration             |
| `05-Internet-Egress/`         | NAT Gateway implementation                    |
| `06-Security/`                | NSGs and Azure security controls              |
| `07-Routing/`                 | Azure and Meridian routing                    |
| `08-Monitoring/`              | Monitoring and logging                        |
| `09-Backup-DR/`               | Backup and disaster recovery                  |
| `10-Testing/`                 | Validation procedures and results             |
| `11-Evidence/`                | Screenshots, captures, CLI output             |
 
---
 
**Folder layout reminder**
 
```text
Azure/
├── 01-Architecture/
│   ├── README.md                 ← this file
│   ├── diagrams/
│   └── screenshots/
├── 02-Networking/
├── 03-Site-to-Site-VPN/
├── 04-Application-Server/
├── 05-Internet-Egress/
├── 06-Security/
├── 07-Routing/
├── 08-Monitoring/
├── 09-Backup-DR/
├── 10-Testing/
└── 11-Evidence/
```
 
