class ResourceManager:
    def __init__(self):
        self.resources = []

    def add_resource(self, name, status):
        self.resources.append({"name": name, "status": status})

    def list_resources(self):
        return self.resources

    def update_resource(self, name, status):
        for resource in self.resources:
            if resource["name"] == name:
                resource["status"] = status
                return True
        return False