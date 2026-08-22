import unittest
import sys
import os

# Set path to import from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from resource_manager import ResourceManager


class TestResourceManager(unittest.TestCase):

    def setUp(self):
        self.manager = ResourceManager()

    def test_add_resource(self):
        resource = self.manager.add_resource("WebServer", "EC2", "running")
        self.assertEqual(len(self.manager.list_resources()), 1)
        self.assertEqual(resource["name"], "WebServer")
        self.assertEqual(resource["type"], "EC2")

    def test_get_resource(self):
        self.manager.add_resource("AppDB", "RDS", "available")
        res = self.manager.get_resource("AppDB")
        self.assertIsNotNone(res)
        self.assertEqual(res["status"], "available")

    def test_update_resource(self):
        self.manager.add_resource("AppDB", "RDS", "available")
        updated = self.manager.update_resource("AppDB", "stopped")
        self.assertTrue(updated)
        self.assertEqual(self.manager.get_resource("AppDB")["status"], "stopped")

    def test_remove_resource(self):
        self.manager.add_resource("OldServer", "EC2", "terminated")
        removed = self.manager.remove_resource("OldServer")
        self.assertTrue(removed)
        self.assertIsNone(self.manager.get_resource("OldServer"))


if __name__ == "__main__":
    unittest.main()