# Change Management Plan: SNMPv2 ----> SNMPv3

## 1. Document Control
*   **Author:** Richard Pateau
*   **Status:** Approved
*   **Date:** 2026-10-27
*   **Target Window:** Tuesday, 08:00 AM - 12:00 PM EST

## 2. Executive Summary & Justification
*   **Business Objective:** Migrate PRTG and Grafana SNMP versions from v2 to v3 for stronger security. 
*   **Risk Profile:** Medium
*   **Scope:** All Core, Distribution, and Access layer switches and routers.
*   **Estimated Downtime:** Zero downtime.

## 3. Pre-Implementation Validation (Pre-Checks)
*Execute these commands prior to the maintenance window to establish a baseline.*

```bash
# HQ-R1
show run | section snmp
show snmp 
show snmp community
```

## 4. Implementation Steps

1. Log into each device.

2. Remove SNMPv2 configuration and replace with SNMPv3:
```config
no snmp-server community prtgadmin
no snmp-server location HQ
no snmp-server contact NOC
no snmp-server ip 172.16.109.1
ip access-list standard 
 10 permit 172.16.109.133
 20 permit 172.16.109.1
snmp-server view PRTG-VIEW iso included
snmp-server group PRTG-GROUP v3 auth read PRTG-VIEW access PRTG-SNMP
snmp-server location Meridian-HQ
snmp-server contact Network-Operations 
snmp-server user **username** PRTG-SNMP v3 auth sha **password** 

```
3. Log into PRTG and update SNMPv3 settings.

4. Update telegraf SNMP settings to match new v3 configurations for Grafana.

## 5. Post-Implementation Validation (Post-Checks)
*Execute these commands immediately after implementation to verify success.*

```bash
show run | section snmp
show snmp 
show snmp | include v3 packets
show snmp community
```

## 6. Rollback / Backout Plan
*Steps required to restore the network to its original state if the migration fails.*

### Step 1: Revert SNMPv3

```config
no ip access-list standard 
no snmp-server view PRTG-VIEW iso included
no snmp-server group PRTG-GROUP v3 auth read PRTG-VIEW access PRTG-SNMP
no snmp-server location Meridian-HQ
no snmp-server contact Network-Operations 
no snmp-server user **username** PRTG-SNMP v3 auth sha **password**
snmp-server community prtgadmin
snmp-server location HQ
snmp-server contact NOC
snmp-server ip 172.16.109.1
```
