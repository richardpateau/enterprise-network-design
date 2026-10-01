# Data Collection

## Overview

Azure Monitor uses a Data Collection Rule to define how monitoring data is collected for the Azure VM.

## Azure Monitor Workspace

| Property | Value                            |
|----------|----------------------------------|
| Name     | defaultazuremonitorworkspace-eus |
| Region   | East US                          |
| Purpose  | Azure Monitor metrics            |

## Data Collection Rule

| Property          | Value                          |
|-------------------|--------------------------------|
| Name              | msvmi-eastus-meridian-az-web01 |
| Region            | East US                        |
| Monitored VM      | MERIDIAN-AZ-WEB01              |
| Collection method | OpenTelemetry-based monitoring |

## OpenTelemetry

Detailed OpenTelemetry metrics were enabled during the VM monitoring configuration.

This provided guest operating-system and resource-level metric visibility beyond basic VM availability.

![workspace](screenshots/monitoring-settings.png)

## Metrics Observed

Following onboarding, the VM produced monitoring data including:

- CPU utilization
- Memory utilization
- Availability
- Process-level CPU
- Host metrics

### Host CPU (validation period)

| Metric  | Value (approx.) |
|---------|-----------------|
| Average | 0.43%           |
| Minimum | 0.27%          |
| Maximum | 0.82%          |

These values represent the observed monitoring period during validation.

![workspace](screenshots/cpu-graph.png)

## Validation

The Monitor page showed populated metric data after onboarding completed successfully.

## Result

The Azure VM was successfully connected to Azure Monitor through the configured monitoring workspace and Data Collection Rule.

## Related Documentation

- [08-Monitoring/README.md](README.md) – Monitoring overview
- [azure-monitor.md](azure-monitor.md) – Azure Monitor configuration
- [metrics.md](metrics.md) – Metrics details
- [alerts.md](alerts.md) – Alert configuration
