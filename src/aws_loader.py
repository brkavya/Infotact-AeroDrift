class AWSLoader:
    def load_resources(self):
        resources = [
            {"type": "VPC", "name": "Main-VPC"},
            {"type": "Subnet", "name": "Public-Subnet"},
            {"type": "EC2", "name": "Web-Server"},
            {"type": "RDS", "name": "Database"}
        ]
        return resources


if __name__ == "__main__":
    loader = AWSLoader()
    for resource in loader.load_resources():
        print(resource)