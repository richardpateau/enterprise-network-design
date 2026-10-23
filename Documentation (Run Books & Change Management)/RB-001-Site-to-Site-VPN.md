## 1. Document Control
*   **Runbook ID:** RB-CFG-001
*   **Devices:** Meridian ASA Firewall to Ashburn's ASA Firewall
*   **Device IPs:** HQ-FW-1 (10.255.110.3), ASH-FW-1 (10.255.112.2)
*   **Primary Owner:** Richard Pateau   

## 2. Prerequisites 

- Reachable IP addresses on both ends 
- Non-overlapping subnet between both locations 
- Underlay routing (OSPF, EIGRP) 
- Authentication Method 
- Crypto Map Parameters

## 3. Pre-Change Checks
- Interfaces (show interface ip brief)
- Failover State (show failover) 
- Existing Tunnel Groups or Crypto Maps 
- Routing (show ip route) 
- Access-lists (show access-lists) 
- NAT (show nat)
 
## 4. Implementation Procedure 

### 1. Configure IKEv2 Policies

**HQ-FW-1**

```cisco
crypto ikev2 policy 10
 encryption aes-256
 integrity sha256
 group 14
 prf sha256
 lifetime seconds 86400
exit
crypto ikev2 enable EDGE-ROUTERS
```

**ASH-FW-1**

```cisco
crypto ikev2 policy 10
 encryption aes-256
 integrity sha256
 group 14
 prf sha256
 lifetime seconds 86400
exit
crypto ikev2 enable ROUTER
```

---

### 2. Configure Tunnel Groups

**HQ-FW-1**

```cisco
tunnel-group 10.255.112.2 type ipsec-l2l
tunnel-group 10.255.112.2 ipsec-attributes
 ikev2 remote-authentication pre-shared-key "Pateau1!"
 ikev2 local-authentication pre-shared-key "Pateau1!"
```

**ASH-FW-1**

```cisco
tunnel-group 10.255.110.3 type ipsec-l2l
tunnel-group 10.255.110.3 ipsec-attributes
 ikev2 remote-authentication pre-shared-key "Pateau1!"
 ikev2 local-authentication pre-shared-key "Pateau1!"
```

---

### 3. Configure IPSec Proposal

**HQ-FW-1**

```cisco
crypto ipsec ikev2 ipsec-proposal MERIDIAN-AES256
 protocol esp encryption aes-256
 protocol esp integrity sha-256
```

**ASH-FW-1**

```cisco
crypto ipsec ikev2 ipsec-proposal MERIDIAN-AES256
 protocol esp encryption aes-256
 protocol esp integrity sha-256
```

---

### 4. Configure Interesting Traffic ACLs

**HQ-FW-1**

```cisco
access-list HQ-ASH-VPN extended permit ip 10.10.0.0 255.255.255.0 10.50.10.0 255.255.255.0
```

**ASH-FW-1**

```cisco
access-list ASH-HQ-VPN extended permit ip 10.50.0.0 255.255.255.0 10.10.10.0 255.255.255.0
```

---

### 5. Configure Crypto Maps

**HQ-FW-1**

```cisco
crypto map MERIDIAN-VPN 10 match address HQ-ASH-VPN
crypto map MERIDIAN-VPN 10 set peer 10.255.112.2
crypto map MERIDIAN-VPN 10 set ikev2 ipsec-proposal MERIDIAN-AES256
crypto map MERIDIAN-VPN interface EDGE-ROUTERS
```

**ASH-FW-1**

```cisco
crypto map MERIDIAN-VPN 10 match address ASH-HQ-VPN
crypto map MERIDIAN-VPN 10 set peer 10.255.110.3
crypto map MERIDIAN-VPN 10 set ikev2 ipsec-proposal MERIDIAN-AES256
crypto map MERIDIAN-VPN interface ROUTER
```

---

### 6. Configure Identity NAT (NAT Exemption)

**HQ-FW-1**

```cisco
object network HQ-NET
 subnet 10.10.0.0 255.255.0.0
object network ASH-NET
 subnet 10.50.0.0 255.255.0.0

nat (HQ-LAN,EDGE-ROUTERS) source static HQ-NET HQ-NET destination static ASH-NET ASH-NET
```

**ASH-FW-1**

```cisco
object network ASH-NET
 subnet 10.50.0.0 255.255.0.0
object network HQ-NET
 subnet 10.10.0.0 255.255.0.0

nat (INTERNAL-ROUTERS,ROUTER) source static ASH-NET ASH-NET destination static HQ-NET HQ-NET
```

---

### 7. Permit Same-Security Traffic (if needed)

**HQ-FW-1**
```cisco
same-security-traffic permit inter-interface
```

**ASH-FW-1**
```cisco
same-security-traffic permit inter-interface
```


## 4. Validation and Post-Change Checks

1) IKEv2 SA's (show crypto ikev2 sa)

2) IPSec SA's (show crypto ipsec sa) - Verify encrypted and decrypted packet numbers

3) Tunnel Group (show run tunnel-group) 

4) End-to-End ICMP Pings from PC (HQ-LAN) to PC (ASHBURN) 

5) Wirehsark pcaps: filter by "ISAKMP" "ESP" "ICMP" 

