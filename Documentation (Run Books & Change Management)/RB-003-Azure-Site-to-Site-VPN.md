## 1. Document Control
*   **Runbook ID:** RB-CFG-003
*   **Devices:** Meridian ASA Firewall to Azure Portal VPN Gateway
*   **Device IPs:** HQ-FW-1 (10.255.110.3)
*   **Primary Owner:** Richard Pateau   

## 2. Prerequisites 

- Reachable IP addresses on both ends 
- Non-overlapping subnet between both locations 
- Routing (ISP ------> Azure Data Center) / Internet Access
- Azure Account & Funding for Resources
- Authentication Methods 
- Crypto Map Parameters

## 3. Pre-Change Checks
- Interfaces (show interface ip brief)
- Failover State (show failover) 
- Existing Tunnel Groups or Crypto Maps 
- Routing (show ip route) 
- Access-lists (show access-lists) 
- NAT (show nat, show run nat) 
 
## 4. Implementation Procedure 

### Configure Resource Group (Mandatory)  
 
**Parameters**

- Subscription = Azure Subscription 1 
- Resource Group Name = Meridian-RG
- Region = East US

### Configure Virtual Network (Mandatory)  
 
**Parameters**

- Subscription = Azure Subscription 1
- Resource Group = Meridian-RG
- Virtual Network Name = Meridian-VNet 
- Address Space = (10.200.10.0/24, 10.200.20.0/24, 10.200.255.0/27) 
- GatewaySubnet = 10.200.255.0/27

### Configure Azure Local Network Gateway (Mandatory)

**Parameters**

- Subscription = Azure Subscription 1 
- IP address = 96.246.138.240

**Addresses**
 
- 10.10.0.0/16 
- 10.20.0.0/16 
- 10.30.0.0/16  
- 10.40.0.0/16  
- 10.50.0.0/16 
- 10.255.0.0/16  
- 172.16.0.0/16
- 192.168.0.0/16 
- 172.31.0.0/16
- 169.254.0.0/16
- 192.0.0.0/8

### Configure Azure NAT Gateway 
- Subscription = Azure Subscription 1 
- Resource Group = Meridian-RG
- Name = Meridian-NAT 
- SKU = StandardV2
- Region = East US 
- Public IP address (IPv4) = Meridian-Public-IP
- Virtual Network = Meridian-VNet

### Configure Azure Virtual Network Gateway 

**Parameters**

- Subscription = Azure Subscription 1 
- Name = Meridian-VPN-Gateway
- Resource Group = Meridian-RG
- Region = East US
- Gateway Type = VPN 
- SKU = VpnGw2AZ

**Public IP Address**
- Create New
- Name = Meridian-Public-IP
- Enable active-active mode = Disabled

### Configure Azure Connections (VPN) 

- Subscription = Azure Subscription 1 
- Resource Group = Meridian-RG
- Connection Type = Site-to-site (IPSec)
- Region = East US
- Name = Meridian-S2S
- Virtual Network Gateway = Meridian-VNG
- Local Network Gateway = Meridian-LNG
- Authentication = PSK
- IKE Protocol = IKEv2

### Configure Static Route 

```cisco
route AZURE-VPN 10.200.0.0 255.255.0.0 172.31.254.2
```
### Configure ikev2 

```cisco
crypto ikev2 policy 10
 encryption aes-256
 integrity sha256
 group 14
 prf sha256
 lifetime seconds 86400
crypto ikev2 enable EDGE-ROUTERS
```

### Configure IPSec Proposal 

```cisco
crypto ipsec ikev2 ipsec-proposal MERIDIAN-AES256
 protocol esp encryption aes-256
 protocol esp integrity sha-256
crypto ipsec profile AZURE-IPSEC-PROFILE
 set ikev2 ipsec-proposal MERIDIAN-AES256
```
### Configure Tunnel-Group 

```cisco
group-policy AZURE-VPN-POLICY internal
group-policy AZURE-VPN-POLICY attributes
 vpn-tunnel-protocol ikev2

tunnel-group 20.81.15.25 type ipsec-l2l
tunnel-group 20.81.15.25 general-attributes
 default-group-policy AZURE-VPN-POLICY
tunnel-group 20.81.15.25 ipsec-attributes
 ikev2 remote-authentication pre-shared-key *******
 ikev2 local-authentication pre-shared-key *******
```

### Configure Virtual Interface (Tunnel100) 

```cisco
interface Tunnel100
 nameif AZURE-VPN
 ip address 172.31.254.1 255.255.255.252 
 tunnel source interface EDGE-ROUTERS
 tunnel destination 20.81.15.25
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile AZURE-IPSEC-PROFILE
```

### Configure NAT Exemption 

```cisco
object network ONPREM-NET
 subnet 10.0.0.0 255.0.0.0          
object network AZURE-NET
 subnet 10.200.0.0 255.255.0.0

nat (inside,EDGE-ROUTERS) source static ONPREM-NET ONPREM-NET destination static AZURE-NET AZURE-NETS no-proxy-arp route-lookup
```
## 4. Validation and Post-Change Checks

1) show crypto ikev2 sa

2) show crypto ipsec sa 

3) show interface Tunnel100

4) show route 

