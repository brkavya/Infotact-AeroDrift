class ResourceManager:
    """Manages cloud resource inventory and state updates."""

    def __init__(self):
        self.resources = []

    def add_resource(self, name: str, resource_type: str, status: str = "active"):
        """Add a new resource to inventory."""
        resource = {"name": name, "type": resource_type, "status": status}
        self.resources.append(resource)
        return resource

    def list_resources(self):
        """Return all tracked resources."""
        return self.resources

    def get_resource(self, name: str):
        """Find a resource by name."""
        for resource in self.resources:
            if resource["name"] == name:
                return resource
        return None

    def update_resource(self, name: str, status: str):
        """Update status of an existing resource."""
        resource = self.get_resource(name)
        if resource:
            resource["status"] = status
            return True
        return False

    def remove_resource(self, name: str):
        """Remove a resource by name."""
        resource = self.get_resource(name)
        if resource:
            self.resources.remove(resource)
            return True
        return False


if __name__ == "__main__":
    manager = ResourceManager()
    manager.add_resource("Web-Server", "EC2", "running")
    manager.add_resource("Database", "RDS", "available")
    print("Initial Resources:", manager.list_resources())
    
    manager.update_resource("Web-Server", "stopped")
    print("Updated Web-Server:", manager.get_resource("Web-Server"))