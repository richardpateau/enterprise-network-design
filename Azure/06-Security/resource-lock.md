# Resource Group Delete Lock

## Resource Group

`Meridian-Azure-RG`

A resource lock was configured to reduce the risk of accidental deletion of the Azure environment.

## Lock Configuration

| Property | Value                        |
|----------|------------------------------|
| Name     | Meridian-Azure-RG-DeleteLock |
| Type     | Delete                       |
| Scope    | Meridian-Azure-RG            |

![Lock](screenshots/resource-lock.png)

## Purpose

The delete lock protects the resource group from accidental deletion.

- It does **not** prevent normal resource configuration or operational changes
- It is intended as an additional administrative safeguard for the Meridian Azure environment

## Validation

The lock was verified in the Azure resource group’s **Locks** configuration and confirmed as active.

![Lock](screenshots/deletion-failure-lock.png)

## Design Notes

- Delete locks are a simple but effective control against accidental removal of critical resources
- The lock can be removed by an authorized administrator if deliberate deletion is required
- Complements the other security controls (NSG, Trusted Launch, Defender for Cloud)

---

### Next Section

Continue to the configuration of virtual machine security features:
- **[Trusted Launch Configuration](trusted_launch.md)** – Secure Boot, vTPM, and integrity monitoring settings.
