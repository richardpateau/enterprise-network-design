# Change Management Plan: [Project Title or Ticket Number]

## 1. Document Control
*   **Author:** [Your Name / Network Engineer]
*   **Status:** Draft / Pending Review
*   **Date:** YYYY-MM-DD
*   **Target Window:** [Date & Time of Maintenance Window]

## 2. Executive Summary & Justification
*   **Business Objective:** [Explain why this change is necessary and what it achieves for the business.]
*   **Risk Profile:** Low / Medium / High
*   **Estimated Downtime:** [Minutes / Hours or "None expected with protocol failover"]

## 3. Pre-Implementation Validation (Pre-Checks)
*Execute these commands prior to the maintenance window to establish a baseline.*
```bash
# [Device Name or Role]
show [command to check current state]
```

## 4. Implementation Steps
*Sequential steps to apply the change.*


## 5. Post-Implementation Validation (Post-Checks)
*Execute these commands immediately after implementation to verify success.*
```bash
show [command to check new state]
```

## 6. Rollback / Backout Plan
*Steps required to restore the network to its original state if the migration fails.*
```config
! Rollback configuration syntax
```
