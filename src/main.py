
from aws_loader import AWSLoader
from resource_manager import ResourceManager


def run_pipeline():
    """Load AWS resources and register them into the Resource Manager."""
    print("Initializing AeroDrift Discovery Pipeline...")
    
    loader = AWSLoader()
    manager = ResourceManager()

    raw_resources = loader.load_resources()
    print(f"Loaded {len(raw_resources)} raw resources from AWS loader.")

    for item in raw_resources:
        manager.add_resource(
            name=item.get("name", "Unknown"),
            resource_type=item.get("type", "Generic"),
            status="discovered"
        )

    print("Current Managed Inventory:")
    for res in manager.list_resources():
        print(f" - [{res['type']}] {res['name']} (Status: {res['status']})")

    return manager


if __name__ == "__main__":
    run_pipeline()