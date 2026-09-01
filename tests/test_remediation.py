import unittest
from src.remediation import RemediationEngine


class TestRemediationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RemediationEngine(
            incident_log_path="logs/test_incidents.log",
            remediation_log_path="logs/test_remediation.log"
        )

    def test_remediate_ec2(self):
        result = self.engine.remediate_resource("EC2", "EC2")
        self.assertTrue(result)

    def test_run_remediation_on_drifted(self):
        mock_status = {
            "EC2": ("Running", "Drifted"),
            "Database": ("Connected", "Healthy"),
        }
        remediation_results = self.engine.run_remediation(mock_status)
        self.assertIn("EC2", remediation_results)
        self.assertEqual(remediation_results["EC2"], "REMEDIATED")


if __name__ == "__main__":
    unittest.main()