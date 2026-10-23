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

### Phase 1: Automation Preparation / Data Entry
*If provisioning via your NetDevOps workflow, update the variable files first.*
1. Open your repository workspace and navigate to the group or host variables file: `inventory/host_vars/[device_name].yml`.
2. Inject the approved parameters:
```yaml
# Host Variables Snippet
target_id: "[ID]"
allocated_vlan: [VLAN_ID]
ip_address: "[IP/Subnet]"
```

### Phase 2: Configuration Syntax / Playbook Execution
*Apply the actual configuration changes using either the automated pipeline or the manual CLI block.*

#### Option A: Automated Execution (Preferred GitOps Method)
Commit the changes to a branch and trigger your pipeline, or run the Ansible playbook locally:
```bash
ansible-playbook -i nautobot_inventory.yml site_provision.yml --limit [device_name]
```

#### Option B: Manual CLI Application (Fallback Method)
If the automation controller is undergoing maintenance, apply this standardized configuration block directly to the terminal:
```config
! Standardized Device Provisioning Block
interface [Interface_ID]
 description [Description_Tag]
 ip address [IP_Address] [Subnet_Mask]
 no shutdown
```

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

### Expected Success Output Baseline:
```text
[Paste a clean text block showing exactly what a healthy, successful command return looks like here]
```

---

## 5. Drift Detection & Compliance Auditing
*How to ensure this newly configured service stays compliant with company baselines over time.*

*   **State Validation:** Run your compliance or state validator playbook daily to verify that manual updates haven't changed these parameters.
```bash
# Run dry-run state validator to check for unapproved configuration drift
ansible-playbook -i nautobot_inventory.yml state_validator.yml --check --diff
```
*   **Security Baseline:** Confirm that all applied access lists (ACLs) or network security groups (NSGs) conform to your enterprise zero-trust model.

