# Change Management Plan: PRTG CPU Threshold Change

## 1. Document Control
*   **Author:** Richard Pateau
*   **Status:** Approved
*   **Date:** 2026-10-27
*   **Target Window:** Tuesday, 08:00 AM - 12:00 PM EST

## 2. Executive Summary & Justification
*   **Business Objective:** To reduce alert fatigue for mild symptoms. 
*   **Risk Profile:** Medium
*   **Scope:** All Core, Distribution, and Access layer switches and routers.
*   **Estimated Downtime:** Zero downtime.

## 3. Pre-Implementation Validation (Pre-Checks)
*Execute these commands prior to the maintenance window to establish a baseline.*

1. 

```bash
# HQ-R1
show run | section snmp
```

2. Check CPU Usage in PRTG Dashboard

## 4. Implementation Steps

1. Go to PRTG Admin Website 

2. Click Devices 

3. Click Device Name: HQ-R1

4. Check CPU Load 

5. Click edit channel

6. Set Upper Error Limit to 90%

7. Set Upper Warning Limit to 80%

8. Configure Notification Settings (Email and/or Ticket)

## 5. Post-Implementation Validation (Post-Checks)
*Execute these commands immediately after implementation to verify success.*

1. Click Device Name: HQ-R1

2. Verify Threshold Settings

3. Trigger simulated threshold to test alerting

## 6. Rollback / Backout Plan
*Steps required to restore the network to its original state if the migration fails.*

### Step 1: Revert PRTF

1. Go to PRTG Admin Website 

2. Click Devices 

3. Click Device Name: HQ-R1

4. Check CPU Load 

5. Click edit channel

6. Leave Upper Error Limit blank or last percentage.

7. Leave Upper Warning Limit blank or last percentage.

8. Revert Notification Settings (Email and/or Ticket)
