## 1. Document Control
*   **Runbook ID:** RB-CFG-002
*   **Devices:** Meridian ASA Firewall to End Device Users (Microsoft Entra ID) 
*   **Device IPs:** HQ-FW-1 (10.255.110.3)
*   **Primary Owner:** Richard Pateau   

## 2. Prerequisites 

- Routing 
- AnyConnect Package External package (external-sso-4.10.08025-webdeploy-k9.pkg) 
- AnyConnect WebGUI package (asdm-7202.bin) 
- Authentication Source (Active Directory)
- VPN Address Pool: 10.10.60.0/24
- MFA 
- Microsoft Entra Ceriticate & Domain Ceritificate
- Mangement Access
- Test PC

## 3. Pre-Change Checks
- show int ip brief
- show run webvpn 
- show run tunnel-group
- show run crypto
- Managmenet PC able to ping and access Web GUI
- Admin Privilege in Microsoft Entra 
- Emergency Console Access 
- test aaa-server authentication <group> host <ip> username <user> password <pw>
- show aaa-server <group>
- Verify Microsoft Entra Users are up to date

## 4. Implementation Procedure
 
### Microsoft Entra ID (Azure AD)

1. Micosoft Entra > Enterprise Apps 
2. Search: **Cisco Secure Firewall - Secure Client**
3. Configure SSO 
   - **Identifier (Entity ID):**  
     `https://labvpn.networkingnotebook.com/saml/sp/metadata/Meridian-Entra-VPN`
   - **Reply URL (Assertion Consumer Service URL):**  
     `https://labvpn.networkingnotebook.com/+CSCOE+/saml/sp/acs?tgname=Meridian-Entra-VPN`
4. Document these values for later:
   - **Login URL:** `https://login.microsoftonline.com/531c7c26-8290-451b-8304-0aee8f075ab2/saml2`
   - **Microsoft Entra Identifier:** `https://sts.windows.net/531c7c26-8290-451b-8304-0aee8f075ab2/`
   - Logout URL: `https://login.microsoftonline.com/531c7c26-8290-451b-8304-0aee8f075ab2/saml2`
5. Download the **Base64 certificate**
6. **Users and groups** > Add the users/groups that require VPN access
7. Create a **Conditional Access** policy > Grant > Require MFA

---

### Enable HTTP Management Access

```cisco
http server enable 8443
http 172.16.109.0 255.255.255.0 HQ-LAN

```

### Certificates

**CLI**
```cisco
crypto ca trustpoint AzureAD-SAML
 revocation-check none
 no id-usage
 enrollment terminal
 no ca-check
crypto ca authenticate AzureAD-SAML
-----BEGIN CERTIFICATE-----
<paste Base64 certificate here>
-----END CERTIFICATE-----
quit
```

Also import public (Let’s Encrypt) identity certificate for `labvpn.networkingnotebook.com` and note its trustpoint name (you will use it as `trustpoint sp`).

**ASDM alternative:**
1) Configuration
2) Device Management
3) Certificate Management
4) CA Certificate > Azure Certificate
5) Identity Certificate > domain (networkingnotebook.com) certificate
---

### ASA – Enable AnyConnect + External Browser

**CLI**
```cisco
webvpn
 anyconnect image disk0:/anyconnect-win-4.x.x-k9.pkg 1
 anyconnect enable
```

**ASDM: Click** 
1) Configuration 
2) Remote Access VPN 
3) Network (Client) Access
4) Secure Client External Browser

**Add: Configuration**
- Browse flash 
- Upload `external-sso-*.pkg`

---

### Address Pool + Split-Tunnel ACL

**CLI**
```cisco
ip local pool Meridian-VPN-Pool 10.60.0.100-10.60.0.199 mask 255.255.255.0

access-list SPLIT-TUNNEL standard permit 172.16.0.0 255.255.0.0
```

**ASDM:** 
1) Configuration
2) Remote Access VPN → Network (Client) Access 
3) Address Assignment 
4) Address Pools

**Add: Configuration**
- Starting IP Address
- Ending IP Address
- Subnet Mask
---

### Group Policy

**CLI**
```cisco
group-policy Meridian-VPN-Policy internal
group-policy Meridian-VPN-Policy attributes
 dns-server value 172.16.109.133
 vpn-tunnel-protocol ssl-client
 default-domain value meridian.local
 split-tunnel-policy tunnelspecified
 split-tunnel-network-list value SPLIT-TUNNEL
 webvpn
  anyconnect ssl external-browser enable
```

**ASDM: Click** 
1) Remote Access VPN 
2) Group Policy 

---

### Tunnel-Group (Connection Profile)

**CLI**
```cisco
tunnel-group Meridian-Entra-VPN type remote-access
tunnel-group Meridian-Entra-VPN general-attributes
 address-pool Meridian-VPN-Pool
 default-group-policy Meridian-VPN-Policy
tunnel-group Meridian-Entra-VPN webvpn-attributes
 authentication saml
 group-alias Meridian-Entra-VPN enable
 saml identity-provider https://sts.windows.net/531c7c26-8290-451b-8304-0aee8f075ab2/
```

**ASDM:** 
1) Configuration
2) Remote Access VPN
3) Network (Client) Access 
4) AnyConnect Connection Profiles  
5) (Set Authentication = SAML, Group Policy, Address Pool, External Browser, etc.)

---

### SAML IdP Configuration

**CLI** (recommended)
```cisco
webvpn
 saml idp https://sts.windows.net/531c7c26-8290-451b-8304-0aee8f075ab2/
  url sign-in https://login.microsoftonline.com/531c7c26-8290-451b-8304-0aee8f075ab2/saml2
  url sign-out https://login.microsoftonline.com/531c7c26-8290-451b-8304-0aee8f075ab2/saml2
  trustpoint idp AzureAD-AC-SAML
  trustpoint sp ASDM_TrustPoint0
  no force re-authentication
  no signature
  base-url https://labvpn.networkingnotebook.com
  timeout assertion 600
```

**ASDM alternative** 

1) Configuration 
2) Remote Access VPN 
3) Network (Client) Access 
4) Secure Client Connection Profiles 
5) Connection Profile (Edit) 

**Configuration Parameters**
- Name = Meridian-Entra-VPN
- Method = SAML
- SAML Server = https://sts.windows.net/531c7c26-8290-451b-8304-0aee8f075ab2/
- IDP Trustpoit = AzureAD-SAML
- SAML Login Experience = VPN Client Embedded Browser
- Group Policy = Meridian-VPN-Policy 
---

### NAT Exemption (Critical)

**CLI**
```cisco
nat (inside,outside) source static any any destination static Meridian-VPN-Pool Meridian-VPN-Pool no-proxy-arp route-lookup
```

---
  
		
## 9. Validation and Post-Change Checks

1) show run webvpn

2) show run tunnel-group Meridian-Entra-VPN

3) show crypto ca certificates

4) show run http 

5) show run group-policy

6) sh ip local pool Meridian-VPN-Pool

---
