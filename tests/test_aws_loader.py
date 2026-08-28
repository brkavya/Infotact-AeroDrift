"""
tests/test_aws_loader.py
Unit tests verifying AWS data loader and relationship extraction.
"""

import unittest
from src.aws_loader import AWSLoader


class TestAWSLoader(unittest.TestCase):

    def setUp(self):
        self.loader = AWSLoader(region_name="us-east-1")

    def test_normalize_ec2_relationships(self):
        raw_ec2 = {
            "id": "i-0123456789abcdef0",
            "vpc_id": "vpc-11223344",
            "subnet_id": "subnet-aabbccdd",
            "security_groups": ["sg-1", "sg-2"]
        }

        normalized = self.loader.normalize_resource(raw_ec2, "EC2")

        self.assertEqual(
            normalized["id"],
            "i-0123456789abcdef0"
        )

        self.assertEqual(
            len(normalized["relationships"]),
            4
        )

        targets = [
            rel["target"]
            for rel in normalized["relationships"]
        ]

        self.assertIn("vpc-11223344", targets)
        self.assertIn("subnet-aabbccdd", targets)
        self.assertIn("sg-1", targets)
        self.assertIn("sg-2", targets)

    def test_ec2_relationship_types(self):
        raw_ec2 = {
            "id": "i-test-01",
            "vpc_id": "vpc-test",
            "subnet_id": "subnet-test",
            "security_groups": ["sg-test"]
        }

        normalized = self.loader.normalize_resource(
            raw_ec2,
            "EC2"
        )

        relationship_types = [
            rel["type"]
            for rel in normalized["relationships"]
        ]

        self.assertIn(
            "CONTAINED_IN",
            relationship_types
        )

        self.assertIn(
            "LOCATED_IN",
            relationship_types
        )

        self.assertIn(
            "ATTACHED_TO",
            relationship_types
        )

    def test_rds_relationships(self):
        raw_rds = {
            "id": "db-test-01",
            "vpc_id": "vpc-test",
            "subnet_group": "dbsubnet-test"
        }

        normalized = self.loader.normalize_resource(
            raw_rds,
            "RDS"
        )

        relationship_types = [
            rel["type"]
            for rel in normalized["relationships"]
        ]

        self.assertIn(
            "CONTAINED_IN",
            relationship_types
        )

        self.assertIn(
            "MEMBER_OF_SUBNET_GROUP",
            relationship_types
        )

    def test_load_resources_returns_normalized_list(self):
        resources = self.loader.load_resources()

        self.assertGreaterEqual(
            len(resources),
            2
        )

        for item in resources:
            self.assertIn("id", item)
            self.assertIn("type", item)
            self.assertIn("relationships", item)


if __name__ == "__main__":
    unittest.main()