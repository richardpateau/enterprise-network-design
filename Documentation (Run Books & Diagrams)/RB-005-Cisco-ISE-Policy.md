## 1. Document Control
*   **Runbook ID:** RB-CFG-005
*   **Devices:** Every Device will be configured with Cisco ISE (802.1X)  
*   **Primary Owner:** Richard Pateau   

## 2. Prerequisites 

- 802.1X is already configured
- Access Ports are documented
- RADIUS Source already set-up (Active Directory) 
- RADIUS already configured on each network device
- Groups segregated in Active Directory (Network-Users, Network-Admins, Guests) 
- Shared Secret for RADIUS Server 
- IP address of each network device that will be enforced via ISE
- MAB devices mac-addresses 
- VLAN assignments 

## 3. Pre-Change Checks
- Mangement IP's (show ip interface brief) 
- VLAN's (show vlan brief) 
- show run | section aaa
- show run | section radius
- show run | section dot1x
- ping < ISE-Server > 
- show ip route (ISE-Server route)  
 
### 4. Implementation Procedure 

### Configure Network Device on Cisco ISE 

**Click:**
- Administration 
- Network Resources
- Network Devices 

**Add: Parameters**
- Name = < device hostname > 
- IP address = < device ip >
- RADIUS Authentication Settings 
- Shared Secret 
- Save 

### Sync Active Directory 

**Click:**
- Administration
- Identity Management
- External Identity Sources 
- Active Directory 

**Parameters**
Joint Point Name = Meridian-AD
Active Directory Domain = meridian.local

### Sync Active Directory Groups 

**Click**
- Administration
- Identity Management
- External Identity Sources
- Meridian-AD
- Groups 
- Add > Select Groups from Directory 

### Create Authorization Profile 

**Click:**
- Policy
- Policy Elements
- Results 
- Authorization > Authorization Profile

**Add: Parameters**
- Name = MERIDIAN-VLAN10
- Access Type = Defualt ACCESS_ACCEPT
- Common Tasks (VLAN Tag 1, ID/Name = 10) 
- Save 

### Apply Policy 

**Click:**
- Policy 
- Policy Sets > Deafult 
- Authorization Policy 

**Parameters**
- Rule Name = VLAN 10 
- Conditions = Permit only Network Users 
- Profiles = MERIDIAN-VLAN10 


## 4. Validation and Post-Change Checks

1) Cisco Live Logs

2) ISE Live Sessions

3) `test aaa group radius vpn.test@meridian.local password *******`
