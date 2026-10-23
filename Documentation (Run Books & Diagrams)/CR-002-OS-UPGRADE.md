# Change Management Plan: Automated OS Upgrade via Ansible

## 1. Document Control
*   **Author:** Richard Pateau	
*   **Status:** Approved
*   **Date:** 2026-10-23
*   **Target Window:** Monday, 08:00 AM - 12:00 PM EST

## 2. Executive Summary & Justification
*   **Business Objective:** Upgrade the switches (C2960S-UNIVERSALK9-M) from Version 15.2(2)E8 to 
Version 15.2(2)E9
*   **Risk Profile:** Medium
*   **Estimated Downtime:** 20 minutes per switch

## 3. Pre-Implementation Validation (Pre-Checks)
*Execute these commands prior to the maintenance window to establish a baseline.*

1. Nautobot Inventory: Ensure that all switches are configured and exist in the Nautobot Invenotry.

2. Storage: Verify that the flash memory in the switches have enough space to retreive .bin update files from TFTP Server.

3. Check Version: `show version` to ensure the current version being used.

4. Perform git commit to ensure that Ansible Playbook syntax (linting) is accurate and perform a DRY RUN locally.


## 4. Implementation Steps

1. Go into the Anisble Directory `cd ~/Ansible`

2. Run a manual DRY RUN `ansible-playbook -i nautobot_inventory.yml os_upgrade.yml --check`

3. If DRY RUN passes run actual playbook `ansible-playbook -i nautobot_inventory.yml os_upgrade.yml`


## 5. Post-Implementation Validation (Post-Checks)
*Execute these commands immediately after implementation to verify success.*

```bash
show flash:
show version
show logging
```

## 6. Rollback / Backout Plan
*Steps required to restore the network to its original state if the migration fails.*

```config
configure terminal
no boot system
boot system flash:/c2960s-universalk9-mz.152-2.E8.bin
do write 
exit
reload
```
