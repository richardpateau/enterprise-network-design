## 1. Document Control
*   **Runbook ID:** RB-CFG-004
*   **Devices:** Meridian ASA Firewalls 
*   **Device IPs:** HQ-FW-1 (10.255.110.3), HQ-FW-2 (10.255.110.4) 
*   **Primary Owner:** Richard Pateau   

## 2. Prerequisites 

- Compatible Software Versions (9.24.x)
- An unused dedicated interface (GigabitEthernet0/5) 
- IP address scheme (Active and Standby IP's) 
- Primary Unit Configurations
- OSPF adjacencies formed 

## 3. Pre-Change Checks
- failover status (show failover) 
- show failover history 
- Both firewalls are directly connected
- Console accessible for emergency accesss
- show version 
- Document `show int ip brief` and `show ospf neighbor` 
 
### 4. Implementation Procedure 

### Configure HQ-FW-1

```cisco
interface GigabitEthernet0/5
 no shutdown
failover
failover lan unit primary
failover lan interface FAILOVER GigabitEthernet0/5
failover key ********
failover link FAILOVER GigabitEthernet0/5
failover interface ip FAILOVER 172.31.255.1 255.255.255.252 standby 172.31.255.2

``` 
### Configure HQ-FW-1

```cisco
interface GigabitEthernet0/5
 no shutdown

failover
failover lan unit secondary
failover lan interface FAILOVER GigabitEthernet0/5
failover key ********
failover link FAILOVER GigabitEthernet0/5
failover interface ip FAILOVER 172.31.255.1 255.255.255.252 standby 172.31.255.2
``` 

### Configure Active / Standby IP Addresses (HQ-FW-1)
*Only two interfaces we're used for this setup, pattern will continure if more interfaces will be used*

**GigabitEthernet0/0**

```cisco
interface GigabitEthernet0/0
 nameif EDGE-ROUTERS
 ip address 10.255.110.3 255.255.255.240 standby 10.255.110.4 
 ipv6 address 2001:db8:10:fd00:1::3/120 standby 2001:db8:10:fd00:1::
``` 
**GigabitEthernet0/2**

```cisco
interface GigabitEthernet0/2
 ip address 10.255.111.1 255.255.255.248 standby 10.255.111.2 
 ipv6 address 2001:db8:10:fd10::3/64 standby 2001:db8:10:fd10::4

``` 

## 4. Validation and Post-Change Checks

1) show failover

2) show failover history 

3) show interface GigabitEthernet0/5

4) show failover interface

