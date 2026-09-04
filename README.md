[![AeroDrift CI](https://github.com/brkavya/Infotact-AeroDrift/actions/workflows/ci.yml/badge.svg)](https://github.com/brkavya/Infotact-AeroDrift/actions/workflows/ci.yml)
# Infotact-AeroDrift
Infotact Python Internship Project
# AeroDrift

## Project Name
Agentic Cloud Topology & Remediation Graph

## Objective
Build a cloud topology graph by collecting AWS resources and representing their relationships using Python.

## Technologies
- Python
- boto3
- NetworkX
- Git
- GitHub

## Project Structure
- src/
- tests/
- docs/

## Current Status
Initial project setup completed.


## Resource Data Contract & Ingestion Schema

The `AWSLoader` (`src/aws_loader.py`) normalizes raw AWS resources into a uniform schema with explicit directional relationships. This feeds directly into `topology.py` for NetworkX graph generation and `resource_manager.py` for inventory tracking:

```json
{
  "id": "i-web-01",
  "type": "EC2",
  "region": "us-east-1",
  "metadata": {
    "name": "Web-Server",
    "vpc_id": "vpc-01",
    "subnet_id": "subnet-01",
    "security_groups": ["sg-web"]
  },
  "relationships": [
    { "target": "vpc-01", "type": "CONTAINED_IN" },
    { "target": "subnet-01", "type": "LOCATED_IN" },
    { "target": "sg-web", "type": "ATTACHED_TO" }
  ]
}

---

## Automated Remediation Engine
The project includes an automated remediation engine (`src/remediation.py`) that evaluates drift states and restores baseline configurations:

- **Baseline Restoration**: Restores drifted compute/database instances to operational baselines.
- **Remediation Audit Logging**: Persists all remediation actions with timestamps to `logs/remediation.log`.

## Running the Project
- **Launch Security & Topology Dashboard**:
  ```bash
  python dashboard.py
```

### Supported Relationship Types
* `CONTAINED_IN` / `PART_OF_VPC`: Parent VPC association.
* `LOCATED_IN`: Subnet placement.
* `ATTACHED_TO`: Security group attachments.
* `MEMBER_OF_SUBNET_GROUP`: DB subnet group associations.
