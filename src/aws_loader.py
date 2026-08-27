"""
src/aws_loader.py
AWS Resource Loader with normalization and directional relationship extraction.
"""

from typing import Dict, List, Any, Optional


class AWSLoader:
    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name

    def normalize_resource(self, raw_data: Dict[str, Any], resource_type: str) -> Dict[str, Any]:
        """
        Normalizes raw AWS resource dictionaries and maps directional dependencies.
        """
        normalized = {
            "id": raw_data.get("id") or raw_data.get("name"),
            "type": resource_type,
            "region": self.region_name,
            "metadata": raw_data,
            "relationships": []
        }

        # EC2 Dependency Mapping
        if resource_type in ("EC2", "AWS::EC2::Instance"):
            if raw_data.get("vpc_id"):
                normalized["relationships"].append({
                    "target": raw_data["vpc_id"],
                    "type": "CONTAINED_IN"
                })
            if raw_data.get("subnet_id"):
                normalized["relationships"].append({
                    "target": raw_data["subnet_id"],
                    "type": "LOCATED_IN"
                })
            for sg in raw_data.get("security_groups", []):
                normalized["relationships"].append({
                    "target": sg,
                    "type": "ATTACHED_TO"
                })

        # Subnet Dependency Mapping
        elif resource_type in ("Subnet", "AWS::EC2::Subnet"):
            if raw_data.get("vpc_id"):
                normalized["relationships"].append({
                    "target": raw_data["vpc_id"],
                    "type": "PART_OF_VPC"
                })

        # RDS Dependency Mapping
        elif resource_type in ("RDS", "AWS::RDS::DBInstance"):
            if raw_data.get("vpc_id"):
                normalized["relationships"].append({
                    "target": raw_data["vpc_id"],
                    "type": "CONTAINED_IN"
                })
            if raw_data.get("subnet_group"):
                normalized["relationships"].append({
                    "target": raw_data["subnet_group"],
                    "type": "MEMBER_OF_SUBNET_GROUP"
                })

        return normalized

    def load_resources(self) -> List[Dict[str, Any]]:
        """
        Loads baseline resources with relationship schemas.
        """
        raw_resources = [
            {
                "id": "i-web-01",
                "name": "Web-Server",
                "type": "EC2",
                "vpc_id": "vpc-01",
                "subnet_id": "subnet-01",
                "security_groups": ["sg-web"]
            },
            {
                "id": "db-prod-01",
                "name": "Database",
                "type": "RDS",
                "vpc_id": "vpc-01",
                "subnet_group": "dbsubnet-01"
            }
        ]

        return [self.normalize_resource(r, r["type"]) for r in raw_resources]


if __name__ == "__main__":
    loader = AWSLoader()
    for resource in loader.load_resources():
        print(resource)