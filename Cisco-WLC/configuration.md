# Cisco WLC Lab — Configuration & Validation Reference

## Overview

This document serves as the technical configuration reference and evidence matrix for the Meridian controller-based wireless implementation. It details the vWLC setup, ISE integration, and the functional validation of both corporate and guest wireless services.

---

## 1. Controller Management & Provisioning

| Setting | Value |
| :--- | :--- |
| **Platform** | Cisco vWLC |
| **Software Version** | 8.7.102.0 |
| **Management IP** | `10.10.70.10/24` (VLAN 70) |
| **Default Gateway** | `10.10.70.1` |
| **Mobility/RF Group** | `Meridian` |
| **Guest Virtual Gateway** | `192.0.2.1` |

*Note: The guest virtual gateway (`192.0.2.1`) is used strictly for web redirection (Captive Portal) and is not the routed default gateway for VLAN 40 clients.*

---

## 2. Access Point Deployment

Physical Cisco Aironet 2802I APs were connected to PoE switches. They successfully obtained IP addresses via DHCP and discovered the vWLC.

**Verification:**
- APs transitioned to the "Registered" state.
- 802.11a/n/ac and 802.11b/g/n radios are enabled and broadcasting.

**AP received DHCP IP upon boot**

![WLC](screenshots/ap-dhcp-ip.png)

**Live AP joining via console***

![WLC](screenshots/ap-joining-live.png)

**AP detected in gui**

![WLC](screenshots/ap-join-gui.png)

**WLC: sh ap summary**

![WLC](screenshots/sh-ap-summary.png)

**WLC: sh advanced 802.11a/b summary**

![WLC](screenshots/sh-802.11.png)

**WLC GUI: 802.11a UP**

![WLC](screenshots/802.11a-up.png)

**WLC GUI: 802.11b UP**

![WLC](screenshots/802.11b-up.png)

---

## 3. Corporate WLAN (802.1X)

| Parameter | Value |
| :--- | :--- |
| **WLAN ID** | 1 |
| **SSID** | `Meridian-Corporate` |
| **Dynamic Interface** | `corp-vlan10` (VLAN 10) |
| **Layer 2 Security** | WPA2/AES |
| **Authentication** | 802.1X (RADIUS) |
| **RADIUS Server** | Cisco ISE (`172.16.109.150`, UDP 1812/1813) |

**ISE Integration:**
The WLC forwards EAPOL frames to ISE. ISE evaluates the user against the `Network-Users` Active Directory group and returns the `MERIDIAN-VLAN10` authorization profile, dynamically assigning the client to VLAN 10.

**Successful sign in: Please enlarge for clearer video**

https://github.com/user-attachments/assets/112f8caf-2f7e-4619-bd21-2da0dc6e4e84

**Wrong password: Please enlarge for clearer video**

https://github.com/user-attachments/assets/79a4933e-8b98-496c-a6c6-0bd5d6783693

![WLC](screenshots/sh-802.11.png)

**Adding WLC to network devices on ISE**

![WLC](screenshots/adding-wlc-ise.png)

**Adding RADUS via ISE to WLAN**

![WLC](screenshots/aaa-authentication.png)

![WLC](screenshots/corporate-aaa-settings.png)

**WLAN GUI: Adding interface for VLAN 10**

![WLC](screenshots/wlan-interfaces.png)

**Mapping VLAN 10 interface to Meridian-Corporate**

![WLC](screenshots/corporate-general.png)

**Meridian-Corporate beacond found**

![WLC](screenshots/sh-802.11.png)

**VLAN 10 IP assigned**

![WLC](screenshots/meridian-corporate-joined.png)

![WLC](screenshots/phone-vlan-10-ip.png)

---

### 4. Guest WLAN (Splash Page & Isolation)

| Parameter | Value |
| :--- | :--- |
| **WLAN ID** | 2 |
| **SSID** | `Meridian-Guest` |
| **Dynamic Interface** | `guest-vlan40` (VLAN 40) |
| **Security** | Open (Web Auth) |
| **Onboarding** | Custom Guest Splash Page |
| **Guest Isolation** | Layer 3 ACL Enforcement |

*Troubleshooting Note: The guest virtual gateway was updated from the default `1.1.1.1` to `192.0.2.1` to resolve web redirection routing issues, after which the passthrough flow functioned correctly.*

### Guest Network Isolation

To protect internal Meridian resources, strict Layer 3 access control lists (ACLs) are applied to guest traffic entering the network via VLAN 40.

**ACL Configuration (GUEST-VLAN40-IN):**
```cisco
Extended IP access list GUEST-VLAN40-IN
    10 permit udp any eq bootpc any eq bootps          ! Allow DHCP
    30 permit tcp 10.10.40.0 0.0.0.255 host 172.16.109.133 eq domain  ! Allow DNS TCP
    40 deny ip 10.10.40.0 0.0.0.255 10.0.0.0 0.255.255.255   ! Block Class A private
    50 deny ip 10.10.40.0 0.0.0.255 172.16.0.0 0.15.255.255  ! Block Class B private
    60 deny ip 10.10.40.0 0.0.0.255 192.168.0.0 0.0.255.255  ! Block Class C private
    70 permit ip 10.10.40.0 0.0.0.255 any                   ! Allow internet access

```
*Troubleshooting Note: The guest virtual gateway was updated from the default `1.1.1.1` to `192.0.2.1` to resolve web redirection routing issues, after which the passthrough flow functioned correctly.*

**Please enlarge for clearer video**

https://github.com/user-attachments/assets/891f2b92-c25b-47c6-bdd4-850c34146110

**Guest VLAN 40 interface created**

![WLC](screenshots/wlan-interfaces.png)

**Mapping VLAN 40 interface to WLAN Meridian-Guest**

![WLC](screenshots/guest-general.png)

**Configuring Web-Policy via Passthrough**

![WLC](screenshots/web-policy.png)

**Customizing Dashboard**

![WLC](screenshots/customized-dashboard.png)

**Captive portal iphone vs PC**

![WLC](screenshots/iphone-captive-portal.png)

![WLC](screenshots/pc-captive-portal.png)

**VLAN 40 IP assigned**

![WLC](screenshots/vlan-40-ip-pc.png)

![WLC](screenshots/vlan-40-ip-iphone.png)

**ISE Live Logs**

![WLC](screenshots/ise-live-logs.png)

**Guest Isolation ACL / Ping**

![WLC](screenshots/vlan-40-acl.png)

![WLC](screenshots/guest-isolation.png)

---

## 5. Evidence

| Verification Stage | Evidence File | What It Proves |
| :--- | :--- | :--- |
| **Architecture** | `wlc-visio.png`, `topology.png` | High-level wireless network topology and architecture. |
| **Hardware** | `physical-ap.jpeg`, `physical-switch.jpeg` | Physical AP and switch deployment. |
| **WLC Setup** | `customized-dashboard.png` | Initial WLC management interface and dashboard. |
| **AP Provisioning** | `ap-dhcp-ip.png` | AP successfully obtains DHCP address. |
| **AP Registration** | `ap-joining-live.png`, `ap-join-gui.png`, `sh-ap-summary.png` | APs successfully establish CAPWAP and register. |
| **WLC Config** | `wlan-interfaces.png`, `corporate-general.png`, `guest-general.png` | WLC WLAN and interface configuration overview. |
| **ISE Integration** | `adding-wlc-ise.png`, `wireless-ise-policy.png`, `corporate-aaa-settings.png` | WLC added as NAD; ISE wireless policy and AAA configured. |
| **Corp Auth Success** | `meridian-corporate-video.mp4` | 🎬 Video: Successful 802.1X auth and VLAN 10 assignment. |
| **Corp Auth Failure** | `wrong-password-video.mp4` | 🎬 Video: ISE correctly rejects invalid credentials. |
| **ISE Live Logs** | `ise-live-logs.png`, `aaa-authentication.png` | ISE RADIUS success logs for wireless clients. |
| **Guest Onboarding** | `iphone-captive-portal.png`, `pc-captive-portal.png` | Custom splash page rendering on client devices. |
| **Guest Video** | `guest-portal-video.mp4` | 🎬 Video: End-to-end guest portal onboarding flow. |
| **Client Validation** | `pc-vlan-10-ip.png`, `phone-vlan-10-ip.png`, `vlan-40-ip-pc.png`, `vlan-40-ip-iphone.png` | Clients receive correct IPs for their respective VLANs. |
| **Guest Isolation** | `guest-isolation.png`, `isolated-guest.png`, `vlan-40-acl.png` | ACLs successfully block guest-to-internal traffic. |
| **WLC Monitoring** | `sh-ap-summary.png`, `sh-802.11.png` | WLC client monitoring and RF summary verification. |

---

## 6. Troubleshooting & Validation Checklist

The following workflows were validated during implementation:
1. **AP Join Failure:** Verified PoE, DHCP scope, and WLC discovery reachability.
2. **802.1X Failure:** Cross-referenced client supplicant settings with ISE Live Logs to identify credential or policy mismatches.
3. **Guest Redirection Failure:** Corrected the WLC Virtual Gateway IP to ensure HTTP intercepts function properly.
4. **Incorrect VLAN Assignment:** Verified the WLC WLAN-to-Interface mapping and switch port trunk configurations.

---

## 7. Operational Security

- RADIUS shared secrets are excluded from this documentation.
- Guest and corporate traffic are strictly segregated via VLANs and ACLs.
- WLC management access should be restricted to the out-of-band management network (VLAN 70) in production.

---
