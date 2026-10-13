# Microsoft 365 Implementation & Validation

## Overview

This document details the configuration and functional validation of the Microsoft 365 environment. It is organized into three phases: Identity & Access Management, Collaboration, and Compliance.

---

## Phase 1: Identity & Access Management (IAM)

### 1.1 User Provisioning & Licensing
A test user was created and provisioned with the appropriate Microsoft 365 licenses to access core applications.

![365](screenshots/new-user-added.png)

![365](screenshots/assigning-license.png)

![365](screenshots/license-overview.png)

### 1.2 Secure Authentication (MFA)
To secure the cloud identity, an authentication method was added and Multi-Factor Authentication (MFA) was enforced. An interrupted authentication test was also captured to demonstrate MFA behavior.

![365](screenshots/added-authentication-method.png)

![365](screenshots/authentication-added.png)

![365](screenshots/enabled-mfa.png)

### 1.3 Administrative Roles
Administrative roles were assigned to the test user to delegate specific management capabilities, adhering to role-based access control (RBAC) principles.

![365](screenshots/assigning-role.png)

---

## Phase 2: Productivity & Collaboration

### 2.1 OneDrive & Exchange
OneDrive administration was configured for cloud storage. Additionally, basic Exchange Online features, such as automatic email replies, were configured and tested.

![365](screenshots/one-drive-overview.png)

![365](screenshots/one-drive-setting.png)

![365](screenshots/automatic-replies.png)

### 2.2 SharePoint Site & Document Management
A dedicated SharePoint site was created to host collaborative document libraries. 

![365](screenshots/creating-sharepoint-site.png)

![365](screenshots/creating-document-library.png)

### 2.3 Version Control & Recovery
SharePoint versioning was enabled to protect against accidental data loss. A functional test was performed to modify a document, view the version history, and successfully recover a previous version.

![365](screenshots/sharepoint-version-control.png)

**Text file change**

![365](screenshots/changed-text.png)

**Version history**

![365](screenshots/text-history.png)

**Older file recovered**

![365](screenshots/text-before-change.png)


---

## Phase 3: Compliance & Auditing

### 3.1 Sign-In Monitoring
Microsoft 365 Sign-In logs were reviewed to verify authentication events and monitor for anomalous access attempts.

![365](screenshots/sign-in-logs.png)


### 3.2 Unified Audit Log
The M365 Audit Log was utilized to track administrative activities. The logs successfully captured activity details, modified properties, and target information for compliance review.

![365](screenshots/audit-log-overview.png)

---

## 4. Evidence Matrix

| Verification Stage | Evidence File | What It Proves |
| :--- | :--- | :--- |
| **Architecture** | `365-visio.png` | Microsoft 365 architecture and workflow diagram. |
| **User & License Mgmt** | `new-user-added.png` | Test user successfully created. |
| | `assigning-license.png` | M365 license assigned to the user. |
| | `license-overview.png` | License details and status confirmed. |
| **Security & MFA** | `adding-authentication-method.png` | Authentication method being added. |
| | `authentication-added.png` | Authentication method successfully configured. |
| | `enable-mfa.png` | MFA successfully enforced for the user. |
| | `assigning-role.png` | Admin role assigned (RBAC). |
| **Productivity** | `one-drive-setting.png` | OneDrive administration/settings configured. |
| | `automatic-replies.png` | Exchange Online auto-reply configured. |
| **SharePoint** | `creating-sharepoint-site.png` | SharePoint site successfully created. |
| | `creating-document-library.png` | Document library created within the site. |
| | `sharepoint-version-control.png` | Document versioning settings enabled. |
| | `text-before-change.png` | Document state captured before modification. |
| | `changed-text.png` | Document successfully modified for testing. |
| | `text-history.png` | Version history accessed and previous content recovered. |
| **Compliance** | `sign-in-logs.png` | Azure AD / M365 Sign-in logs reviewed. |
| | `audit-log-overview.png` | Unified Audit Log interface accessed. |
| | `audit-logs.png` | Specific audit log activities and details captured. |
