# Azure Monitor

## Purpose

Azure Monitor provides centralized monitoring for the Meridian Azure infrastructure.

For this project, Azure Monitor was configured on the `MERIDIAN-AZ-WEB01` application server to collect VM and guest operating-system metrics.

## Monitored VM

| Property         | Value                    |
|------------------|--------------------------|
| Name             | MERIDIAN-AZ-WEB01        |
| Resource Group   | Meridian-Azure-RG        |
| Region           | East US                  |
| Operating System | Ubuntu Server 24.04 LTS  |
| Private IP       | 10.200.10.4              |
| Subnet           | Azure-Apps               |

## Monitoring Configuration

Enhanced monitoring was initially unavailable until monitoring was configured from the VM Monitor page.

The configuration enabled:

- OpenTelemetry detailed metrics
- Azure Monitor workspace integration
- Data Collection Rule
- Grafana dashboard support
- Recommended metric alerts

![workspace](screenshots/monitor-settings.png)

### Workspace

```text
defaultazuremonitorworkspace-eus
```

### Data Collection Rule

```text
msvmi-eastus-meridian-az-web01
```
![workspace](screenshots/monitoring-workspace.png)

## Onboarding

Azure reported:

```text
Onboarding successful
```

After onboarding completed, the VM Monitor page began displaying monitoring data.

## Metrics Collected

The monitoring configuration populated data for:

- CPU utilization
- Memory utilization
- VM availability
- Process-level CPU metrics
- Host metrics

![workspace](screenshots/cpu-graph.png)

## Result

Azure Monitor was successfully configured for the Meridian application server and began reporting VM and guest operating-system metrics.

## Related Documentation

- [08-Monitoring/README.md](README.md) – Monitoring overview
- [data-collection-rule.md](data-collection-rule.md) – Data Collection Rule details
- [metrics.md](metrics.md) – Metrics details
- [alerts.md](alerts.md) – Alert configuration
