# 03 – Site-to-Site VPN

## Overview

The Meridian Financial Services environment uses an Azure site-to-site IPsec VPN to provide private connectivity between the on-premises Meridian network and the Azure environment.

The VPN connects the Meridian HQ firewall HA pair to an Azure VPN Gateway using **IKEv2** and **IPsec**.

## VPN Architecture

```text
Meridian On-Premises
        |
   HQ-EDGE-1
        |
  HQ-FW-1 / HQ-FW-2
        |
     Internet
        |
 Azure VPN Gateway
        |
 Meridian-Azure-VNet
   10.200.0.0/16
```

## VPN Components

| Component              | Configuration          |
|------------------------|------------------------|
| Azure VPN Gateway      | Microsoft-Azure-VGW    |
| Gateway SKU            | VpnGw2AZ               |
| Gateway Type           | Route-based            |
| Active-Active          | Enabled                |
| Local Network Gateway  | Meridian-OnPrem-LNG1   |
| Azure Connection       | Meridian-Azure-S2S     |
| On-Premises Public IP  | 96.246.138.240         |
| Azure Public IP 1      | 20.81.15.25            |
| Azure Public IP 2      | 135.222.248.148        |
| VPN Protocol           | IKEv2 / IPsec          |
| Authentication         | Pre-shared key         |
| Azure VNet             | Meridian-Azure-VNet    |
| Azure VNet Address Space | 10.200.0.0/16        |

## VPN Design

- Azure side uses a route-based VPN Gateway
- On-premises ASA uses a route-based IPsec VTI for the Azure connection

```text
HQ-FW-1 (10.255.110.3)
        |
   Tunnel100
   172.31.254.1/30
        |
   IPsec / IKEv2
        |
Azure VPN Gateway (20.81.15.25)
        |
   10.200.0.0/16
```

## Security Parameters

| Setting              | Value                  |
|----------------------|------------------------|
| IKE Version          | IKEv2                  |
| Encryption           | AES-256                |
| Integrity            | SHA-256                |
| Diffie-Hellman Group | 14                     |
| IPsec Encryption     | AES-256                |
| IPsec Integrity      | SHA-256                |
| Authentication       | Pre-shared key         |
| NAT-T                | Enabled where required |

The pre-shared key is intentionally not documented in this repository.

## Implementation Status

Configured and validated:

- Azure VPN Gateway
- Azure Local Network Gateway
- Azure site-to-site connection
- ASA IKEv2 configuration
- ASA IPsec proposal / profile
- ASA VTI (Tunnel100)
- Azure peer tunnel group
- Successful bidirectional IKEv2 negotiation

Packet capture evidence confirms successful IKEv2 negotiation.

## Documentation Structure

```text
03-Site-to-Site-VPN/
├── README.md                 ← this file
├── azure-vpn-gateway.md
├── local-network-gateway.md
├── vpn-connection.md
├── asa-vti.md
├── ikev2.md
├── ipsec.md
└── screenshots/
```

## Related Documentation

| Document                  | Description                          |
|---------------------------|--------------------------------------|
| `azure-vpn-gateway.md`    | Azure VPN Gateway configuration      |
| `local-network-gateway.md`| Local Network Gateway                |
| `vpn-connection.md`       | Site-to-site connection              |
| `asa-vti.md`              | ASA route-based VTI                  |
| `ikev2.md`                | IKEv2 policy and negotiation         |
| `ipsec.md`                | IPsec proposals and profiles         |
| `screenshots/`            | Supporting screenshots and captures  |

## Related Sections

- [01-Architecture](../01-Architecture/) – Overall hybrid architecture
- [02-Networking](../02-Networking/) – VNet and subnet design
- [07-Routing](../07-Routing/) – Hybrid routing details
