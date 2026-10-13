# Azure NAT Gateway

## Overview

`Meridian-AZ-NAT` provides outbound Internet connectivity for workloads deployed in the Azure application subnet.

The NAT Gateway is associated with the `Azure-Apps` subnet and uses a dedicated public IP address for outbound Network Address Translation.

## Configuration

| Property          | Value                 |
|-------------------|-----------------------|
| Name              | `Meridian-AZ-NAT`     |
| VNet              | `Meridian-Azure-VNet` |
| Associated Subnet | `Azure-Apps`          |
| Subnet Address    | `10.200.10.0/24`      |
| Public IP         | `MERIDIAN-NAT-PIP`    |
| Application VM    | `MERIDIAN-AZ-WEB01`   |
| VM Private IP     | `10.200.10.4`         |
| VM Public IP      | None                  |

## Network Placement

```text
Meridian-Azure-VNet
10.200.0.0/16
        |
        v
Azure-Apps
10.200.10.0/24
        |
        v
Meridian-AZ-NAT
        |
        v
MERIDIAN-NAT-PIP
        |
        v
Internet
```

## Purpose

The NAT Gateway was deployed to provide outbound Internet connectivity for the Azure application workload.

The application VM does not require a public IP address to initiate outbound connections.

## Problem Before NAT Gateway

Before the NAT Gateway was deployed, the Azure VM did not have working outbound Internet connectivity.

Package repository access failed when attempting to update the Ubuntu system.

Example:

```bash
apt update
```

The VM could communicate with its private Azure network but did not have functional outbound Internet access.

## NAT Gateway Deployment

The `Meridian-AZ-NAT` NAT Gateway was created and associated with:

| Property | Value                 |
|----------|-----------------------|
| VNet     | `Meridian-Azure-VNet` |
| Subnet   | `Azure-Apps`          |
| Address  | `10.200.10.0/24`      |

A dedicated public IP resource was associated with the NAT Gateway:

```text
MERIDIAN-NAT-PIP
```

## Verification

After the NAT Gateway was associated with `Azure-Apps`, outbound Internet connectivity was successfully established.

The Ubuntu package repositories became reachable and the following command completed successfully:

```bash
apt update
```

The system successfully downloaded package metadata from the Internet.

This confirmed that the NAT Gateway was providing functional outbound Internet connectivity.

## Security Model

The application VM remains private:

```text
MERIDIAN-AZ-WEB01
10.200.10.4
```

No public IP is assigned directly to the VM.

The NAT Gateway provides outbound translation while the VM's inbound traffic remains governed by its Network Security Group and private network connectivity.


## Related Documentation

- [README.md](README.md) – Internet egress overview
- [02-Networking](../02-Networking/) – VNet and subnet design
- [04-Application-Server](../04-Application-Server/) – Application VM
- [06-Security](../06-Security/) – Network Security Groups
