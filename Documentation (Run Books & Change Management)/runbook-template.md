# Configuration Runbook: [Service, Asset, or Protocol Provisioning]

## 1. Document Control
*   **Runbook ID:** RB-CFG-[Number]
*   **Target Domain:** [e.g., Enterprise Switch Fabric / Azure Hybrid Core / Automation / Nautobot]
*   **Primary Owner:** [Your Name / Automation Team]
*   **Classification:** Standard Operating Procedure (SOP)
*   **Version Baseline:** [e.g., Cisco IOS-XE 17.09.x / Ansible 2.15 / Terraform v1.5]

---

## 2. Prerequisites & Pre-Flight Checklist
*Do not apply configurations until every item on this list is fully verified.*

1. **Inventory Reservation:** Ensure the target node is correctly listed and set to `Active` state inside the Source of Truth database (Nautobot / NetBox).
2. **Resource Allocation:** Reserve the necessary IP subnets, VLAN IDs, and BGP ASNs in your IPAM tracker to prevent overlaps.
3. **Connectivity Verification:** Confirm management reachability to the node from the automation controller or jump host.

```bash
# Check basic device reachability before pushing configuration modifications
ping [Device_IP_or_FQDN]
```

---

## 3. Step-by-Step Configuration Implementation


---

## 4. Post-Configuration Verification (Show Commands)
*Execute these verification steps to prove the service was provisioned successfully and is functioning correctly.*

```bash
# Verify physical interface status and line protocol state
show interface [Interface_ID] status

# Verify IP addressing tables and routing binding
show ip interface brief | exclude unassigned

# Verify database protocol synchronization
show [protocol_name] summary
```
