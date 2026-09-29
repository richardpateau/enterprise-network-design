# 04 – Application Server

## Overview

The Meridian Azure environment includes an application server hosted in Microsoft Azure.

The server provides a private web application workload that is accessible only through the Meridian hybrid network (site-to-site VPN).

## Application Server

| Property          | Value                      |
|-------------------|----------------------------|
| Server Name       | MERIDIAN-AZ-WEB01          |
| Operating System  | Ubuntu Server 24.04 LTS    |
| Azure Region      | East US                    |
| VM Size           | Standard_D2as_v4           |
| VNet              | Meridian-Azure-VNet        |
| Subnet            | Azure-Apps                 |
| Subnet Address    | 10.200.10.0/24             |
| Private IP        | 10.200.10.4                |
| Public IP         | None                       |
| Web Server        | Apache HTTP Server         |

## Network Placement

The application server is deployed in the dedicated Azure application subnet:

```text
Meridian-Azure-VNet (10.200.0.0/16)
            |
       Azure-Apps (10.200.10.0/24)
            |
     MERIDIAN-AZ-WEB01
         10.200.10.4
```

## Application

Apache HTTP Server is installed on the Ubuntu VM.

The server hosts a custom Meridian Financial Services webpage that describes the Azure workload and its hybrid network placement.

## Access

The VM has no public IP address.

- Administrative access is performed over the private network using SSH
- Application access (HTTP) is intended from the Meridian network via the site-to-site VPN

```text
Meridian Network
        |
   Site-to-Site VPN
        |
    Azure VNet
        |
   10.200.10.4
        |
   SSH / HTTP
```

## Security

The Azure VM is protected by a Network Security Group (NSG).

Initial HTTP rule:

| Setting          | Value               |
|------------------|---------------------|
| Rule Name        | Allow-Meridian-HTTP |
| Source           | 10.0.0.0/8          |
| Destination Port | 80/TCP              |
| Action           | Allow               |
| Priority         | 1010                |

Full NSG details are documented in 06-Security/.

## Implementation Status

### Completed

- Azure VM deployed
- Ubuntu Server 24.04 LTS installed
- Private IP assigned (10.200.10.4)
- No public IP assigned
- SSH access tested over private network
- Apache HTTP Server installed and running
- Custom Meridian webpage deployed
- HTTP access permitted via NSG from Meridian address space

## Documentation Structure

```text
04-Application-Server/
├── README.md              ← this file
├── azure-vm.md
├── web-server.md
└── screenshots/
```

## Related Documentation

| Document        | Description                    |
|-----------------|--------------------------------|
| `azure-vm.md`   | Azure VM configuration details |
| `web-server.md` | Apache installation and webpage |
| `screenshots/`  | Supporting screenshots         |

## Related Sections

- [01-Architecture](../01-Architecture/) – Overall hybrid architecture
- [02-Networking](../02-Networking/) – VNet and subnet design
- [03-Site-to-Site-VPN](../03-Site-to-Site-VPN/) – Hybrid connectivity
- [05-Internet-Egress](../05-Internet-Egress/) – NAT Gateway outbound access
- [06-Security](../06-Security/) – NSG and security controls
