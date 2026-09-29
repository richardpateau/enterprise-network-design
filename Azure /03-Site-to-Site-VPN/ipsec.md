# IPsec

## Overview

IPsec provides the encrypted data plane for the Meridian-to-Azure site-to-site VPN.

The Cisco ASA uses an IPsec proposal and profile associated with the Azure VTI (`Tunnel100`).

## IPsec Proposal

```cisco
crypto ipsec ikev2 ipsec-proposal MERIDIAN-AES256
 protocol esp encryption aes-256
 protocol esp integrity sha-256
```

## IPsec Parameters

| Parameter   | Value     |
|-------------|-----------|
| Protocol    | ESP       |
| Encryption  | AES-256   |
| Integrity   | SHA-256   |
| PFS         | None      |
| IKE Version | IKEv2     |

## IPsec Profile

```cisco
crypto ipsec profile AZURE-IPSEC-PROFILE
 set ikev2 ipsec-proposal MERIDIAN-AES256
```

![SHOW RUN](screenshots/sh-run-ipsec.png)

The profile is applied to the Azure VTI:

```text
Tunnel100 (AZURE-VPN)
```

## NAT Traversal

During IKE negotiation, NAT detection was observed. The VPN subsequently used UDP port 4500 for encrypted traffic.

```text
UDP/500
    |
    | IKE negotiation
    v
UDP/4500
    |
    | NAT-T / encrypted VPN traffic
    v
IPsec tunnel
```

## Azure Peer & Tunnel Interface

| Item             | Value           |
|------------------|-----------------|
| Azure Peer       | 20.81.15.25     |
| Tunnel Interface | Tunnel100       |
| Nameif           | AZURE-VPN       |
| Tunnel IP        | 172.31.254.1/30 |

## Separation from Existing VPN

The Azure IPsec configuration is completely separate from the existing Meridian site-to-site VPN crypto-map configuration.

- Existing crypto-map remains unchanged
- Azure connection uses the VTI’s dynamically generated crypto-map

## Evidence

The IKEv2/IPsec packet capture provides evidence of successful negotiation:

- IKE_SA_INIT
- IKE_AUTH
- Encrypted and Authenticated payloads
- UDP/4500 NAT-T traffic

Packet capture location (filter by "ISAKMP"):

```text
pcaps/azure-ikev2-negotiation.pcap
```

## Design Notes

- Parameters (AES-256 / SHA-256 / no PFS) are aligned with the Azure connection settings 
- Profile is bound only to Tunnel100 so it does not affect other VPNs

## Related Documentation

- [asa-vti.md](asa-vti.md) – ASA route-based VTI
- [ikev2.md](ikev2.md) – IKEv2 policy and negotiation
- [vpn-connection.md](vpn-connection.md) – Azure site-to-site connection
- [azure-vpn-gateway.md](azure-vpn-gateway.md) – Azure VPN Gateway
