# Recovery Services Vault

## Purpose

Azure Recovery Services Vault provides the backup storage and management location for protected Azure workloads.

The Meridian Azure environment uses a Recovery Services vault to protect the application server.

## Vault Configuration

| Property                   | Value                      |
|----------------------------|----------------------------|
| Name                       | Meridian-AZ-RecoveryVault  |
| Resource Group             | Meridian-Azure-RG          |
| Region                     | East US                    |
| Backup storage redundancy  | GRS                        |
| Cross Region Restore       | Disabled                   |
| Immutability               | Disabled                   |

![geo redundant](screenshots/recovery-services-overview.png)

## Backup Storage

The vault uses **geo-redundant storage (GRS)**.

This provides geographically redundant backup storage for the protected workload.

![geo redundant](screenshots/geo-redundant.png)

## Protected Workload

The following VM is protected by the vault:

```text
MERIDIAN-AZ-WEB01
```

## Recovery Model

The vault provides recovery points that can be used to restore the protected VM.

For this project, a recovery point was successfully used to create a separate restored VM for disaster recovery validation.

## Result

The Recovery Services vault was successfully created and used to protect the Meridian Azure application server.

---

### Next Section

Continue to the final validation of the backup and disaster recovery process:
- **[Restore Test & Validation](restore-test.md)** – Step-by-step recovery point restoration and post-restore application validation.
