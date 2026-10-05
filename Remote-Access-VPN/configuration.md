# Remote Access VPN Implementation & Validation

## Overview

This document details the configuration and functional validation of the Meridian Remote Access VPN. The implementation is divided into three core phases: Identity Integration, ASA Gateway Configuration, and End-to-End Application Testing.

---

## Phase 1: Identity & SAML Integration

To ensure secure authentication, the Cisco ASA was integrated with the Meridian identity infrastructure using SAML SSO.

### 1.1 Directory Synchronization
Active Directory was synchronized with Microsoft Entra ID. This included configuring User Principal Names (UPNs), enabling password synchronization, and verifying user presence in the Entra tenant.

**Downloading Connect Sync via Entra ID**

![Remote Access](screenshots/hq-fw1-ikev2-sa.png)

**Applying UPN for Entra ID**

![Remote Access](screenshots/applying-upn.png)

**Connecting AD via Connect Sync**

![Remote Access](screenshots/connecting-ad.png)

**Enabling password sync**

![Remote Access](screenshots/password-sync.png)

**Live sync progression**

![Remote Access](screenshots/sync-process.png)

**Users in Active Directory**

![Remote Access](screenshots/hq-fw1-ikev2-sa.png)

**AD users successfully added to Entra ID**

![Remote Access](screenshots/entra-users.png)

### 1.2 SAML & Certificate Configuration
The Cisco ASA was registered as an Enterprise Application in Entra ID. The SAML SSO configuration was finalized by downloading the base64 SSO certificate from the IdP and installing it onto the ASA's crypto CA trustpoint.

![Remote Access](screenshots/vbase64-cert.png)

![Remote Access](screenshots/certs-used-base64.png)

### 2.1 SAML Sign-In and Sign-Out URLs
To complete the SAML integration, the Identity Provider (IdP) Sign-In and Sign-Out URLs (acquired from Entra ID) were applied to the Cisco ASA. 

This ensures that when a user initiates a connection, they are correctly redirected to the Entra login page, and when they disconnect, the ASA properly terminates the SAML session with the IdP.

![Remote Access](screenshots/sign-in-out.png)

---

## Phase 2: ASA Gateway Configuration

The Cisco ASA was configured to terminate AnyConnect sessions and enforce access policies.

### 2.1 Group Policy & Connection Profiles
A dedicated Group Policy was created to define client parameters (DNS, split-tunnel rules). A corresponding Connection Profile was configured to link the AnyConnect client to the SAML identity provider and the specific Group Policy.

![Remote Access](screenshots/group-policy.png)

### 2.2 Address Pool & Access Control
A specific IP address pool was configured to assign virtual IPs to remote clients upon successful authentication. A VPN ACL was applied to the Group Policy to strictly limit the remote users' access to authorized internal subnets.

![Remote Access](screenshots/address-pool-config.png)

![Remote Access](screenshots/address-pools.png)

![Remote Access](screenshots/vpn-acl.png)

### 2.3 CLI Verification
Post-configuration, the ASA was verified via CLI to confirm the WebVPN status, tunnel-group parameters, and crypto CA certificate installation.

![Remote Access](screenshots/sh-run-webvpn.png)

![Remote Access](screenshots/sh-run-tunnel-group.png)

![Remote Access](screenshots/sh-crypto-ca.png)

---

## Phase 3: Client Deployment & Application Testing

An internal Apache web server was deployed to act as a protected resource for end-to-end validation.

![Remote Access](screenshots/apache-server.png)

### 3.1 AnyConnect Authentication
The Cisco AnyConnect client was deployed to a remote endpoint. The user successfully authenticated via the SAML SSO flow, establishing an encrypted tunnel and receiving an IP address from the configured VPN pool.

![Remote Access](screenshots/sh-vpn-session-anyconnect.png)

### 3.2 Positive Access Test
With the VPN tunnel active, the remote client successfully accessed the internal Apache web server, proving that the tunnel routing and VPN ACLs are functioning correctly.

**Please enlarge for clearer video**

https://github.com/user-attachments/assets/7d1570e3-e0d5-493a-9c50-fc34d82003b4

![Remote Access](screenshots/successful-sign-in.png)

### 3.3 Negative Access Test (Zero Trust Validation)
The VPN tunnel was disconnected. The remote client attempted to access the Apache web server again. The connection failed, proving that the internal resource is strictly protected and inaccessible without active VPN authentication.

![Remote Access](screenshots/apache-fail-no-vpn.png)

---

## 4. Evidence

| Verification Stage | Evidence File | What It Proves |
| :--- | :--- | :--- |
| **Architecture** | `remote-access-visio.png` | Remote Access VPN network topology. |
| **Identity Integration** | `connecting-ad.png` | Active Directory connection configuration. |
| | `ad-users.png` | Active Directory user directory. |
| | `entra-users.png` | Microsoft Entra ID user synchronization. |
| | `applying-upn.png` | User Principal Name (UPN) configuration. |
| | `sync-process.png` | Directory synchronization process. |
| | `password-sync.png` | Password synchronization enabled. |
| | `ad-connect-sync.png` | Azure AD Connect synchronization tool. |
| **SAML & Certificates** | `base64-cert.png` | Base64 SSO certificate downloaded from IdP. |
| | `certs-used-base64.png` | Certificates used for SAML integration. |
| | `sign-in-out.png` | SAML Sign-In and Sign-Out URLs applied to ASA. |
| **ASA Configuration** | `asa-group-policy.png` | ASA Group Policy configuration. |
| | `asa-address-pools.png` | Remote access VPN address pool assignment. |
| | `vpn-acl.png` | VPN Access Control List for traffic restriction. |
| **ASA CLI Verification** | `sh-run-tunnel-group.png` | CLI verification of tunnel group parameters. |
| | `sh-run-webvpn.png` | CLI verification of WebVPN/AnyConnect settings. |
| | `sh-crypto-ca.png` | CLI verification of installed SSO certificates. |
| | `sh-vpn-session-anyconnect.png` | CLI verification of active AnyConnect user sessions. |
| **Client Connection** | `successful-sign-in.png` | AnyConnect client successful SSO authentication. |
| | `video/anyconnect.mp4` | Dynamic video proof of the AnyConnect sign-in process. |
| **Application Testing** | `apache-server.png` | Internal Apache web server configuration. |
| | `apache-fail-no-vpn.png` | **Negative Test:** Protected resource blocked without active VPN. |

---

## 5. End-to-End Validation Workflow

![IPSec](screenshots/remote-access-visio-2.png)

---

## 6. Scope & Boundaries

This document validates the **operational state and functional access** of the Remote Access VPN. 

It does not document the underlying Entra ID tenant configuration details or specific ASA crypto-map commands, as those are outside the scope of this operational validation evidence.
