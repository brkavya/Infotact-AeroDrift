class HealthChecker:
    """Evaluates the operational health and risk score of cloud resources."""

    def __init__(self):
        self.health_records = {}

    def check_status(self, resource: dict) -> dict:
        """Evaluate resource health based on type and current state."""
        name = resource.get("name", "unknown")
        res_type = resource.get("type", "generic")
        status = resource.get("status", "unknown").lower()

        if status in ["running", "available", "active"]:
            health = "HEALTHY"
            risk_score = 0.1
        elif status in ["stopped", "degraded"]:
            health = "WARNING"
            risk_score = 0.6
        else:
            health = "CRITICAL"
            risk_score = 0.9

        record = {
            "resource_name": name,
            "resource_type": res_type,
            "health": health,
            "risk_score": risk_score,
        }
        self.health_records[name] = record
        return record

    def get_all_records(self) -> dict:
        """Return all evaluated health records."""
        return self.health_records


if __name__ == "__main__":
    checker = HealthChecker()
    sample_ec2 = {"name": "Web-Server", "type": "EC2", "status": "running"}
    sample_rds = {"name": "Database", "type": "RDS", "status": "stopped"}

    print("EC2 Health:", checker.check_status(sample_ec2))
    print("RDS Health:", checker.check_status(sample_rds))