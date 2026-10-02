Here is the polished, portfolio-ready version of your `stp-verification.md`. 

Just like the VLAN document, I have transformed this from a "lab checklist" into a formal **engineering validation report**. It clearly separates steady-state topology verification from dynamic convergence testing, which is exactly what hiring managers look for when evaluating network resiliency.

***

# STP Operational Verification & Convergence Testing

## Objective

Validate that Spanning Tree Protocol (STP) is operating according to the Meridian Layer 2 topology design. Verification ensures a loop-free environment, predictable root bridge election, optimal port roles, and rapid convergence during topology changes.

---

## 1. Topology & Root Bridge Verification (Steady State)

The foundation of a stable Layer 2 network is a predictable root bridge. The following commands verify the global STP topology.

### Root Bridge Election
**Command:** `show spanning-tree root`

**Validation Criteria:**
* Confirms **HQ-SW-1** is the primary Root Bridge for all documented VLANs.
* Verifies optimal Root Path Cost from downstream switches.
* Confirms correct Root Port selection on non-root switches.
* Ensures no unintended switches have assumed the root role due to priority misconfigurations.

### Detailed Port Roles & States (VLAN 10)
**Command:** `show spanning-tree vlan 10`

**Validation Criteria:**
* **Root Ports (RP):** Verified on downstream switches pointing toward HQ-SW-1.
* **Designated Ports (DP):** Verified on all trunk links forwarding traffic away from the root.
* **Alternate/Blocking Ports:** Verified on redundant links to ensure a loop-free topology without blocking legitimate primary paths.
* **Forwarding State:** Confirmed that all active root and designated ports are in the `FWD` state.

---

## 2. Edge Port Protection Verification

To ensure rapid host connectivity and prevent accidental loops, edge ports must be strictly isolated from the core STP topology.

**Command:** `show spanning-tree interface Ethernet1/0 detail`

**Validation Criteria:**
* **PortFast:** Confirmed as `enabled` on endpoint-facing access ports, allowing immediate transition to the forwarding state.
* **BPDU Guard:** Confirmed as `enabled` to protect the edge.
* **Scope:** Verified that PortFast and BPDU Guard are **excluded** from infrastructure trunks and EtherChannel links, preserving legitimate STP BPDUs between switches.

*(Note: Detailed BPDU Guard failure testing is documented in the `BPDU-Guard/` directory).*

---

## 3. Functional Convergence Testing (Resiliency)

Operational state only proves the network is healthy *today*. Functional testing proves the network will survive a failure *tomorrow*. 

A controlled topology change was executed to validate STP convergence behavior.

### Test Methodology
1. **Pre-Failure State:** Captured baseline STP port roles, forwarding states, and initiated a continuous ping to the default gateway.
2. **Failure Injection:** Intentionally shut down the active Root Port (or primary trunk link) on a downstream switch.
3. **Post-Failure State:** Captured the new STP topology, verifying the Alternate port transitioned to Root Port/Forwarding state.

### Convergence Results
* **Topology Update:** The downstream switch successfully identified the loss of the primary path and promoted the Alternate port to Root Port.
* **Traffic Restoration:** The continuous ping experienced a brief, acceptable interruption (sub-second to a few seconds, depending on STP mode) before successfully restoring Layer 2 connectivity.
* **Loop Prevention:** No broadcast storms or MAC flapping were observed during the transition.

**HQ-SW-1**
![STP](screenshots/hq-sw1-stp-vlan10-after.png)

---

## 4. Evidence & Artifacts

### Operational Screenshots
Representative steady-state verification screenshots are stored in:
`Switching/Verification/STP/screenshots/`

**Recommended Evidence:**
* `hq-sw1-show-spanning-tree-root.png` *(Proves HQ-SW-1 root bridge election)*
* `hq-sw2-show-spanning-tree-vlan10.png` *(Proves correct Root/Designated/Alternate port roles)*
* `hq-sw1-e1-0-stp-detail.png` *(Proves PortFast/BPDU Guard edge protection)*

### Functional Test Evidence
The raw convergence testing evidence (pre-failure, failure injection, and post-failure states) is maintained in the project-level testing directory:
`STP Testing/` *(or `Switching/STP/` depending on your exact folder structure)*

---

## Verification Conclusion

STP verification confirms the intended Layer 2 topology is successfully implemented. HQ-SW-1 is correctly elected as the root bridge, port roles are optimally assigned, edge ports are protected via PortFast/BPDU Guard, and the network demonstrates predictable, loop-free convergence during simulated link failures.

***

