from aws_loader import AWSLoader
from resource_manager import ResourceManager
from health_check import HealthChecker


def run_pipeline():
    """Execute end-to-end resource discovery, inventory registration, and health evaluation."""
    print("=== Starting AeroDrift Discovery & Health Pipeline ===")
    
    loader = AWSLoader()
    manager = ResourceManager()
    checker = HealthChecker()

    # 1. Discover raw AWS resources
    raw_resources = loader.load_resources()
    print(f"[+] Loaded {len(raw_resources)} resources from AWS loader.")

    # 2. Register resources in manager inventory
    for item in raw_resources:
        manager.add_resource(
            name=item.get("name", "Unknown"),
            resource_type=item.get("type", "Generic"),
            status="active"
        )

    # 3. Evaluate health and risk for each managed resource
    print("\n--- Managed Inventory & Health Status ---")
    for res in manager.list_resources():
        health_record = checker.check_status(res)
        print(
            f" - Resource: {res['name']:<12} | "
            f"Type: {res['type']:<6} | "
            f"Health: {health_record['health']:<8} | "
            f"Risk: {health_record['risk_score']}"
        )

    print("\n=== Pipeline Execution Completed Successfully ===")
    return manager, checker


if __name__ == "__main__":
    run_pipeline()