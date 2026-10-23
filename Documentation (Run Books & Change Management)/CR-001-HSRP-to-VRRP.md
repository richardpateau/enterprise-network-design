# Change Management Plan: HSRP ----> VRRP

## 1. Document Control
*   **Author:** Richard Pateau
*   **Status:** Approved
*   **Date:** 2026-10-22
*   **Target Window:** Monday, 08:00 AM - 12:00 PM EST

## 2. Executive Summary & Justification
*   **Business Objective:** The goal is to migrate HSRP to VRRP so the company to prevent vendor lock-in. 
*   **Risk Profile:** Medium
*   **Estimated Downtime:** Under 5 minutes. 

## 3. Pre-Implementation Validation (Pre-Checks)
*Execute these commands prior to the maintenance window to establish a baseline.*
```bash
# HQ-R1
show standby brief
show standby 
show ip interface brief
show run | section interface 

```

## 4. Implementation Steps

1. Log into HQ-R1

2. Remove HSRP Commands and add VRRP Commands:
```config
interface f0/0.10
 no standby version 2
 no standby 10 ip 10.10.10.1
 no standby 10 priority 110
 no standby 10 preempt
 vrrp 10 ip 10.10.10.1 
 vrrp 10 preempt
 vrrp 10 priority 110
```
3. Log into HQ-R2

4. Remove HSRP Commands and add VRRP Commands:
```config
interface f0/0.10
 no standby version 2
 no standby 10 ip 10.10.10.1
 no standby 10 priority 100
 no standby 10 preempt
 vrrp 10 ip 10.10.10.1 
 vrrp 10 preempt
 vrrp 10 priority 100
```

## 5. Post-Implementation Validation (Post-Checks)
*Execute these commands immediately after implementation to verify success.*
```bash
show vrrp brief
show run interface int f0/0.10 

#From a PC 
ping 10.10.10.1
ping 10.10.10.2 (HQ-R1)
ping 10.10.10.3 (HQ-R2)
```

## 6. Rollback / Backout Plan
*Steps required to restore the network to its original state if the migration fails.*

### Step 1: Revert HQ-R1 to HSRP 

```config
interface f0/0.10
 no vrrp 10
 standby version 2
 standby 10 ip 10.10.10.1
 standby 10 priority 110
 standby 10 preempt
```
### Step 1: Revert HQ-R2 to HSRP

```config
interface f0/0.10
 no vrrp 10
 standby version 2
 standby 10 ip 10.10.10.1
 standby 10 priority 100
 standby 10 preempt
```
