import unittest
import sys
import os

# Set path to import from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from health_check import HealthChecker


class TestHealthChecker(unittest.TestCase):

    def setUp(self):
        self.checker = HealthChecker()

    def test_healthy_resource(self):
        ec2 = {"name": "Web-Server", "type": "EC2", "status": "running"}
        record = self.checker.check_status(ec2)
        self.assertEqual(record["health"], "HEALTHY")
        self.assertLessEqual(record["risk_score"], 0.2)

    def test_warning_resource(self):
        rds = {"name": "Database", "type": "RDS", "status": "stopped"}
        record = self.checker.check_status(rds)
        self.assertEqual(record["health"], "WARNING")
        self.assertEqual(record["risk_score"], 0.6)

    def test_critical_resource(self):
        unknown_res = {"name": "Cache", "type": "Redis", "status": "failed"}
        record = self.checker.check_status(unknown_res)
        self.assertEqual(record["health"], "CRITICAL")
        self.assertGreaterEqual(record["risk_score"], 0.8)


if __name__ == "__main__":
    unittest.main()