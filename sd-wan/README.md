graph TD
    %% Styling
    classDef fortinet fill:#ee3b2e,stroke:#333,stroke-width:2px,color:white,font-weight:bold;
    classDef isp fill:#f39c12,stroke:#333,stroke-width:2px,color:white,font-weight:bold;
    classDef lan fill:#3498db,stroke:#333,stroke-width:2px,color:white,font-weight:bold;
    classDef endpoint fill:#2ecc71,stroke:#333,stroke-width:2px,color:white,font-weight:bold;
    classDef capture fill:#9b59b6,stroke:#333,stroke-width:2px,color:white,font-weight:bold,stroke-dasharray: 5 5;

    %% HQ Site
    subgraph HQ Site [🏢 Headquarters (HQ)]
        direction TB
        HQ-PC[🖥️ HQ Server\nUbuntu / iPerf3]:::endpoint
        HQ-SW[🔀 L2 Switch\nVLAN 10]:::lan
        FG-HQ[🛡️ FortiGate 60F/VM\nHQ Gateway]:::fortinet
        HQ-PC ---|Eth0/1| HQ-SW
        HQ-SW ---|Eth0/24 Trunk| FG-HQ
    end

    %% WAN / Underlay
    subgraph WAN Underlay [🌐 WAN / ISP Underlay]
        direction TB
        ISP1-Left[📡 ISP-1 Router\nMPLS]:::isp
        ISP2-Left[📡 ISP-2 Router\nBroadband]:::isp
        ISP1-Right[📡 ISP-1 Router\nMPLS]:::isp
        ISP2-Right[📡 ISP-2 Router\nBroadband]:::isp
        
        ISP1-Left ===|10.0.1.0/30| ISP1-Right
        ISP2-Left ===|10.0.2.0/30| ISP2-Right
    end

    %% Branch Site
    subgraph Branch Site [🏬 Branch Office]
        direction TB
        FG-BR[🛡️ FortiGate 60F/VM\nBranch Gateway]:::fortinet
        BR-SW[🔀 L2 Switch\nVLAN 20]:::lan
        BR-PC[💻 Branch Client\nUbuntu + Wireshark]:::endpoint
        
        FG-BR ---|Eth0/24 Trunk| BR-SW
        BR-SW ---|Eth0/1| BR-PC
    end

    %% SD-WAN Overlay Connections
    FG-HQ ===|WAN1: MPLS\n10.0.1.2| ISP1-Left
    FG-HQ ===|WAN2: BB\n10.0.2.2| ISP2-Left
    FG-BR ===|WAN1: MPLS\n10.0.1.1| ISP1-Right
    FG-BR ===|WAN2: BB\n10.0.2.1| ISP2-Right

    %% PCAP Capture Points
    CP1(((📸 PCAP 1\nClient LAN))):::capture
    CP2(((📸 PCAP 2\nWAN1 MPLS))):::capture
    CP3(((📸 PCAP 3\nWAN2 BB))):::capture

    BR-PC -.-> CP1
    FG-HQ -.-> CP2
    FG-HQ -.-> CP3

    %% Legend
    subgraph Legend [📌 Legend]
        L1[🛡️ FortiGate SD-WAN]:::fortinet
        L2[📡 Underlay Router]:::isp
        L3[🔀 LAN Switch]:::lan
        L4[💻 Endpoint]:::endpoint
        L5[📸 Wireshark Capture Point]:::capture
    end
