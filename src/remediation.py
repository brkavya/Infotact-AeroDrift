from pathlib import Path
from datetime import datetime


class RemediationEngine:
    def __init__(self, incident_log_path="logs/incidents.log", remediation_log_path="logs/remediation.log"):
        self.incident_log = Path(incident_log_path)
        self.remediation_log = Path(remediation_log_path)

    def log_action(self, resource: str, action: str, status: str):
        self.remediation_log.parent.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.remediation_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Resource: {resource} | Action: {action} | Status: {status}\n")

    def remediate_resource(self, resource_name: str, resource_type: str) -> bool:
        """Applies baseline restoration based on resource type."""
        if resource_type == "EC2":
            # Simulate restoring instance baseline settings / security group association
            self.log_action(resource_name, "Restored baseline security group and operational state", "SUCCESS")
            return True
        elif resource_type == "RDS":
            self.log_action(resource_name, "Reset connection limits and synchronized baseline", "SUCCESS")
            return True
        else:
            self.log_action(resource_name, "Generic drift remediation applied", "SUCCESS")
            return True

    def run_remediation(self, resource_status_dict: dict) -> dict:
        """Scans resources and remediates any marked as Drifted."""
        results = {}
        for resource, (status, health) in resource_status_dict.items():
            if health == "Drifted":
                success = self.remediate_resource(resource, "EC2" if resource == "EC2" else "General")
                results[resource] = "REMEDIATED" if success else "FAILED"
        return results