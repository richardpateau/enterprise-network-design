# Windows DNS & Group Policy Implementation

## Overview

This document details the configuration and validation of Windows DNS and Group Policy within the Meridian environment. It covers domain integration, name resolution testing, and the deployment of critical security baselines via GPO.

---

## 1. Active Directory Domain Integration

To receive Group Policies and utilize domain DNS, endpoints must be joined to the Meridian Active Directory domain. 

**Implementation:**
A Windows 10 client was successfully joined to the domain and placed into the appropriate Organizational Unit (OU) for policy application.

![DNS](screenshots/adding-windows-to-dc.png)

![DNS](screenshots/adding-windows-to-dc-2.png)

---

## 2. DNS Infrastructure & Resolution

Windows DNS is the backbone of Active Directory. We configured both Forward and Reverse lookup zones to ensure comprehensive name resolution.

### 2.1 Forward & Reverse Lookups
- **Forward Lookup:** Resolves hostnames (e.g., `win10-pc.meridian.local`) to IP addresses.
- **Reverse Lookup:** Resolves IP addresses back to hostnames using PTR records. This is critical for certain security and logging applications.

![DNS](screenshots/dns-forward-lookup.png)

![DNS](screenshots/dns-reverse-lookup.png)

### 2.2 Cross-Platform Validation
To ensure the DNS infrastructure is robust, resolution was tested from both native Windows clients and an Alpine Linux client. Both successfully resolved internal Meridian records and external queries.

![DNS](screenshots/nslookup-desktop.png)

![DNS](screenshots/nslookup-test-a-record.png)

![DNS](screenshots/nslookup-google.png)

![DNS](screenshots/windows-nslookup.png)

![DNS](screenshots/windows-nslookup-google.png)
---

## 3. Group Policy & Security Baselines

Group Policy Objects (GPOs) were created to enforce the Meridian Security Baseline. This ensures that every device joining the domain automatically receives the required security posture.

![DNS](screenshots/gpo-overview.png)

### 3.1 Windows Defender Firewall & ICMP
A GPO was configured to manage Windows Defender Firewall settings centrally. 
- **Objective:** Standardize firewall rules and allow ICMP (Ping) traffic specifically from the Meridian management network (`10.0.0.0/8`) to facilitate network monitoring and troubleshooting.

**Defender Overview**

![DNS](screenshots/defender-gpo-overview.png)

**ICMP rules added to GPO**

![DNS](screenshots/defender-icmp-rule.png)

**Rule automatically mapped to defender firewall list**

![DNS](screenshots/defender-rule-overview.png)

### 3.2 Password Policy
To protect domain credentials, a strict password policy was enforced:
- Minimum password length enforced (e.g., 12 characters).
- Complexity requirements enabled.

![DNS](screenshots/password-policy.png)

**Validation:** A test user attempting to set a weak password (`Test123456!`) was rejected by the system. A compliant password (`Q5/wV*3D'Z5$`) was successfully accepted.

**Test123456!**

![DNS](screenshots/password-fail.png)

**Please enlarge for clearer video**

**Q5/wV*3D'Z5$**

![DNS](screenshots/password-success.png)

**Please enlarge for clearer video**


### 3.3 Account Lockout Policy
To mitigate brute-force attacks, an account lockout policy was configured to temporarily disable accounts after a defined number of failed authentication attempts.

![DNS](screenshots/account-lockout.png)

---

## 4. Client-Side Policy Verification

It is not enough to configure a GPO; we must verify it actually applies to the endpoint. 

**Validation:**
PowerShell (`gpresult /r`) was executed on the Windows 10 client to confirm that the Meridian GPOs were successfully downloaded and applied to the local machine.

![DNS](screenshots/successful-gpo-windows.png)

---

**Evidence Checklist:**

**Domain Integration:**
- [x] `adding-windows-to-dc.png` (Proof of Windows 10 client successfully joining Meridian AD)
- [x] `adding-windows-to-dc-2.png` (Proof of computer object correctly placed in AD OU)

**DNS Configuration & Validation:**
- [x] `dns-overview.png` (Proof of DNS server/zone configuration)
- [x] `dns-forward-lookup.png` (Proof of forward lookup zone functioning)
- [x] `dns-reverse-lookup.png` (Proof of reverse lookup zone functioning)
- [x] `windows-nslookup.png` / `nslookup-desktop.png` (Proof of Windows client resolving names successfully)
- [x] `nslookup-test-a-record.png` (Proof of cross-platform/Alpine client resolving A records)
- [x] `nslookup-google.png` / `windows-nslookup-google.png` (Proof of external DNS forwarding/resolution)

**GPO Architecture & Application:**
- [x] `dns-gpo-visio.png` (Proof of DNS/GPO architecture diagram)
- [x] `gpo-overview.png` (Proof of GPO structure in Group Policy Management)
- [x] `successful-gpo-windows.png` (Proof of `gpresult` confirming GPO application on client)

**Firewall & Network (Defender):**
- [x] `defender-gpo-overview.png` (Proof of Defender Firewall configured via GPO)
- [x] `defender-rule-overview.png` (Proof of firewall rules successfully applied to client)
- [x] `defender-icmp-rule.png` (Proof of ICMP allowed from `10.0.0.0/8` network)

**Security Baselines & Testing:**
- [x] `password-policy.png` (Proof of password complexity policy configured)
- [x] `account-lockout.png` (Proof of account lockout threshold configured)
- [x] `password-fail.png` (Proof of weak password correctly rejected by OS)
- [x] `password-success.png` (Proof of compliant password correctly accepted)

**Dynamic Video Evidence:**
- [x] `password-fail-video.mp4` (Live proof of password rejection behavior)
- [x] `password-success-video.mp4` (Live proof of password acceptance behavior)

---

## 6. Scope & Boundaries

This section documents **Windows DNS and Group Policy**.

**Not covered here:**
- DHCP Scope Management (covered in `01-DHCP/`)
- NTFS/File Share Permissions (covered in `03-File-Shares/`)
- Event Log Auditing & SIEM (covered in `04-Logging-SIEM/`)
