# Infotact-AeroDrift

## AeroDrift – Agentic Cloud Topology & Remediation Graph

### Project Overview

AeroDrift is a Python-based CloudOps project designed to monitor cloud resources, visualize infrastructure topology, detect resource configuration drift, and generate incident reports.

The project uses graph-based modeling to represent relationships between cloud resources such as EC2 instances, VPCs, subnets, databases, and security groups.

---

## Objective

The objective of AeroDrift is to:

- Build a cloud infrastructure topology graph.
- Represent cloud resource relationships using NetworkX.
- Load and normalize AWS resource data.
- Monitor resource health.
- Detect configuration drift.
- Display security alerts.
- Generate structured incident reports.
- Log incidents automatically.
- Provide a terminal-based monitoring dashboard.

---

## Technologies Used

- Python
- boto3
- NetworkX
- Rich
- Git
- GitHub
- pytest

---

## Project Features

### Cloud Topology

- Represents cloud resources as graph nodes.
- Represents relationships between resources as graph edges.
- Displays topology statistics.

### Resource Monitoring

- Monitors Compute, Database, and Network resources.
- Detects resource health status.
- Identifies configuration drift.

### Security Monitoring

- Calculates security score.
- Displays security alerts.
- Identifies high-risk resources.

### Incident Management

- Generates structured incident reports.
- Provides incident summaries.
- Displays incident severity breakdown.
- Automatically logs incidents.

### Dashboard

The Rich-powered terminal dashboard displays:

- Cloud topology overview.
- Cloud resources.
- Resource health status.
- Health summary.
- Resource statistics.
- Security assessment.
- Security alerts.
- Incident reports.
- Incident summary.
- Incident severity breakdown.
- Final system status.

---

## Project Structure

```text
AeroDrift-Team
│
├── dashboard.py
├── topology.py
├── README.md
├── requirements.txt
│
├── logs
│   └── incidents.log
│
├── src
│   ├── aws_loader.py
│   ├── health_check.py
│   ├── main.py
│   └── resource_manager.py
│
└── tests
    ├── test_aws_loader.py
    ├── test_health_check.py
    ├── test_resource_manager.py
    └── test_topology.py