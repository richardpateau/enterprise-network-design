# Windows File Shares — Implementation & Validation

## Overview

This document details the configuration of Windows File Shares and the rigorous functional testing performed to validate Role-Based Access Control (RBAC) via NTFS permissions in the Meridian environment.

---

## 1. File Share & NTFS Configuration

To enforce granular access control, permissions are evaluated at the NTFS level. 

### 1.1 Share Configuration
A dedicated file share was created to host Meridian network resources. Share-level permissions were configured to allow baseline access, delegating the actual access control to NTFS.

### 1.2 NTFS Permissions
Granular NTFS permissions were applied to the folder. This ensures that even if a user bypasses the network share, the underlying file system enforces the security boundary.

![File Share](screenshots/nfts-permissions.png)

---

## 2. Identity Mapping

Access is dictated by the authenticated Windows identity. Two distinct identities were used for validation:

1. **Network Administrator:** A privileged account granted Full Control/Modify rights.
   
   ![Network Admin Identity](screenshots/network-admin-shares.png)
   
2. **802.1X Network User:** A standard domain account granted Read & Execute rights.
   
   ![Network User Identity](screenshots/network-user-share.png)

---

## 3. Functional Validation: Network Administrator

The administrator account was tested to verify full management capabilities.

- **Write/Modify:** Successfully edited an existing file.
  
  **Please enlarge for clearer video**

  https://github.com/user-attachments/assets/f1a60925-6aff-44ef-b04b-1053acdbaae0

- **Create/Delete:** Successfully created a new file and subsequently deleted it.
  
  **Please enlarge for clearer video**

  https://github.com/user-attachments/assets/71a86de9-49cf-473b-a7bf-8d13078ca982

**Result:** Administrative access controls are functioning as designed.

---

## 4. Functional Validation: 802.1X Network User (Negative Testing)

Negative testing is critical to prove that permissions are actively enforced, not just configured. The standard user account was tested against the same share.

### 4.1 Read Access
Successfully opened and read a file from the share.

![Read Successful](screenshots/read-successful.png)

### 4.2 Write Access (DENIED)
Attempted to modify the file. The OS explicitly denied the action.

https://github.com/user-attachments/assets/1522c632-2694-4d01-9f12-606014ad3c2c

![Write Denied Screenshot](screenshots/unable-to-write.png)

### 4.3 Create Access (DENIED)
Attempted to create a new file in the directory. The OS explicitly denied the action.

![Unable to Create](screenshots/unable-to-create.png)

**Result:** The Principle of Least Privilege is successfully enforced.

## 5. Evidence Repository

### Architecture & Configuration
- [x] `file-share-visio.png` — File share access model diagram.
- [x] `nfts-permissions.png` — Granular NTFS permissions configured correctly.
- [x] `network-admin-shares.png` — Share-level permissions established (Admin context).
- [x] `network-user-share.png` — Share-level permissions established (User context).

### Admin Validation (Positive Testing)
- [x] `write-privilege.mp4` — Video proof of admin write/modify privileges.
- [x] `share-permissions.gif` — Animated proof of admin share access.
- [x] `creating-file.mp4` — Video proof of admin successfully creating a file.

### User Validation (Read Access)
- [x] `read-successful.png` — Standard user can successfully read files.

### User Validation (Negative Testing)
- [x] `unable-to-write.png` — Standard user write attempts blocked (Screenshot).
- [x] `write-denied-screenshot.png` — Additional screenshot of write denial.
- [x] `write-denied.mp4` — Video proof of standard user write attempts blocked.
- [x] `unable-to-create.png` — Standard user create attempts blocked.

---

## 6. Identity Continuity Note

The "802.1X Network User" referenced in this testing is the same identity authenticated by Cisco ISE in the `02-802.1X/` module. This demonstrates **identity continuity**: a user authenticates to the network via 802.1X, receives a VLAN assignment, and then seamlessly uses those same Windows domain credentials to access file shares with permissions dictated by Active Directory group membership.

---

## 7. Scope & Boundaries

This section documents **Windows File Share and NTFS permission enforcement**.

**Not covered here:**
- 802.1X Network Access Control configuration (covered in `Cisco-ISE/02-802.1X/`)
- Active Directory Group Policy creation (covered in `Windows/02-DNS-GPO/`)
