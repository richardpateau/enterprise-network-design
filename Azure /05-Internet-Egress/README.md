# 05 – Internet Egress

## Overview

The Meridian Azure environment uses an Azure NAT Gateway to provide controlled outbound Internet connectivity for Azure workloads **without** assigning public IP addresses directly to the workloads.

The NAT Gateway is associated with the Azure application subnet that contains `MERIDIAN-AZ-WEB01`.

## Configuration

| Property            | Value                  |
|---------------------|------------------------|
| NAT Gateway         | Meridian-AZ-NAT        |
| Public IP           | MERIDIAN-NAT-PIP       |
| VNet                | Meridian-Azure-VNet    |
| Associated Subnet   | Azure-Apps             |
| Subnet Address      | 10.200.10.0/24         |
| Application VM      | MERIDIAN-AZ-WEB01      |
| VM Private IP       | 10.200.10.4            |
| VM Public IP        | None                   |

## Architecture

```text
MERIDIAN-AZ-WEB01 (10.200.10.4)
            |
       Azure-Apps (10.200.10.0/24)
            |
      Meridian-AZ-NAT
            |
      MERIDIAN-NAT-PIP
            |
         Internet
```

## Design

The NAT Gateway provides outbound Internet connectivity while keeping the Azure application server private.

- MERIDIAN-AZ-WEB01 has no public IP address
- Outbound connections are source-NAT’d through the NAT Gateway’s public IP
- The VM can reach external services (package repositories, updates, etc.) without being directly reachable from the Internet

This design supports the architecture principle of private application workloads with controlled egress.

## Implementation

- NAT Gateway (Meridian-AZ-NAT) was deployed
- Public IP (MERIDIAN-NAT-PIP) was associated with the NAT Gateway
- NAT Gateway was associated with the Azure-Apps subnet

Before: The Azure VM had no functional outbound Internet connectivity.  
After: Outbound Internet connectivity was established via the NAT Gateway.

## Verification

Outbound connectivity was verified by running:

```bash
apt update
```

The command successfully contacted the Ubuntu package repositories after the NAT Gateway was associated with the subnet.

This confirmed functional outbound Internet access from the private Azure VM.

## Security Considerations

- Outbound Internet access is provided without assigning a public IP to the application VM
- Inbound access remains controlled by the Network Security Group and the private hybrid network design
- The VM is not directly Internet-addressable

## Documentation Structure

```text
05-Internet-Egress/
├── README.md              ← this file
├── nat-gateway.md
└── screenshots/
```

## Related Documentation

| Document          | Description                        |
|-------------------|------------------------------------|
| `nat-gateway.md`  | NAT Gateway configuration details  |
| `screenshots/`    | Supporting screenshots             |

## Related Sections

- [01-Architecture](../01-Architecture/) – Overall hybrid architecture
- [02-Networking](../02-Networking/) – VNet and subnet design
- [04-Application-Server](../04-Application-Server/) – Application VM
- [06-Security](../06-Security/) – Network Security Groups
