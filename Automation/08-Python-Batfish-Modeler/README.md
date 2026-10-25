# Pre-Deployment Network Modeling & Reachability Validation (Batfish)

## Summary
Pushing configuration changes to a network based solely on text-based diffs is a massive operational risk. This project implements **Batfish**, an open-source, vendor-agnostic network modeling engine, to mathematically simulate packet flows through proposed configurations. By building an offline digital twin of the network, this Python validator proves that intended traffic (SSH) is reachable and malicious traffic (Telnet) is explicitly blocked *before* the configuration is ever deployed to physical hardware.

**SSH being blocked (intentional failure): Please enlarge for clearer video**

https://github.com/user-attachments/assets/0ca8c7f9-aa42-4fb7-befb-6e6505e1a056

**Telnet not being blocked (intentional failure): Please enlarge for clearer video**

https://github.com/user-attachments/assets/33e74d75-7349-4585-b756-d51483bf982d

---

## ️ Architecture & Design Patterns

### 1. Offline Digital Twin Modeling
Unlike traditional tools that SSH into live devices, Batfish runs locally in a Docker container. It ingests raw Cisco IOS/Firepower configurations, builds a mathematical model of the control and data planes (routing tables, ACLs, NAT), and allows for instantaneous, risk-free querying.

![Automation](screenshots/topology.png)

![Automation](screenshots/each-config-file.png)

### 2. Advanced Packet Flow Simulation
Using `pybatfish`'s `HeaderConstraints` and `PathConstraints`, the script injects simulated packets at specific ingress interfaces (e.g., `@enter(HQ-EDGE-1)`). It traces the packet through the entire forwarding path, evaluating:
*   Ingress/Egress ACLs
*   Routing table lookups
*   NAT translations
*   Firewall zone policies

### 3. CI/CD Ready Exit Codes
The script is designed to act as a hard gate in a CI/CD pipeline. It distinguishes between fatal parsing errors and non-fatal warnings. If a reachability test fails (e.g., SSH is blocked), the script triggers `sys.exit(1)`, instantly failing the GitHub Actions pipeline and blocking the deployment.

---

##  Workflow Diagram

![Automation](screenshots/batfish-visio.png)

---

## Key Technical Features

*   **Modern Pybatfish Data Models:** Utilizes `HeaderConstraints` and `PathConstraints` for precise packet injection and flow tracing.
*   **Interface-Level Injection:** Uses `startLocation='@enter(HQ-EDGE-1)'` to simulate traffic entering the network at the exact physical boundary.
*   **Action-Based Validation:** Explicitly checks for `SUCCESS` and `DENIED_IN` actions in the flow traces, proving the firewall ACLs are functioning as intended.
*   **Strict CI/CD Integration:** Returns non-zero exit codes on validation failure, making it a perfect drop-in gate for GitHub Actions or GitLab CI.

![Automation](screenshots/path-constraints.png)

![Automation](screenshots/start-location.png)

![Automation](screenshots/denied-in.png)

![Automation](screenshots/sys-exit.png)

---

## Prerequisites & Setup

1. **Docker:** Required to run the `batfish/batfish` container locally.
2. **Python Environment:** Python 3.8+ with `pybatfish` installed (`pip install pybatfish`).
3. **Configuration Snapshots:** A directory containing the raw `.cfg` files for the network devices (Routers, Switches, Firewalls).

![Automation](screenshots/batfish-docker.png)

---

## Evidence 

Below is visual proof of the Batfish modeling and reachability validation workflow.

### 1. Pre-Deployment State

**The firewall ACL configuration before the proposed changes, allowing SSH management**

![Automation](screenshots/fw-config-before.png)

**The interface configuration on the router before changes**

![Automation](screenshots/r1-acl-before.png)

### 2. Successful Reachability Validation

**The Python script successfully simulating the network. SSH is reachable (SUCCESS) and Telnet is blocked (DENIED_IN)**

![Automation](screenshots/terminal-success.png)

### 3. Intentional Failure Testing 

**To prove the validator works, an intentional failure was introduced: removing the IP access-group from the router interface**

![Automation](screenshots/r1-acl-intentional-failure.png)

**The Batfish script correctly identifies that the device is no longer reachable in the modeled network and fails the test**

![Automation](screenshots/terminal-fail-acl.png)

**Testing a strict "Deny IP Any Any" rule on the firewall to ensure SSH is blocked**

![Automation](screenshots/fw-intentional-config-fail.png)

![Automation](screenshots/terminal-fail-ssh.png)

### Execution Videos
*   [Batfish Intentional ACL Fail - Router](media/batfish-intentional-acl-fail-r1-2026-10-20_01.25.03.mp4)
*   [Batfish Intentional Fail - Firewall](media/batfish-intentional-fail-fw-2026-10-20_01.23.22.mp4)

---

### What's Next?

With pre-deployment mathematical modeling and CI/CD safety gates fully integrated, the automation lifecycle is complete. The final step is to explore the standardized operational procedures and change management processes that govern this enterprise environment.

Continue to the final section to explore operational documentation:
- **[Documentation (Run Books & Change Management)](../../Documentation%20(Run%20Books%20&%20Change%20Management)/)** – Standardized Change Requests (CR), Run Books (RB), and enterprise operational procedures.
