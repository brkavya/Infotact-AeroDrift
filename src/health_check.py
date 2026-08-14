class HealthCheck:
    def __init__(self):
        self.status = {
            "EC2": "Running",
            "RDS": "Available",
            "S3": "Accessible"
        }

    def get_status(self):
        return self.status

    def display_status(self):
        print("Cloud Resource Health Status")
        for resource, state in self.status.items():
            print(f"{resource}: {state}")


if __name__ == "__main__":
    health = HealthCheck()
    health.display_status()