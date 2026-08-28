import unittest
from topology import initialize_cloud_topology


class TestCloudTopology(unittest.TestCase):

    def setUp(self):
        self.graph = initialize_cloud_topology()

    def test_aws_resource_nodes(self):
        self.assertIn("i-web-01", self.graph.nodes)
        self.assertIn("db-prod-01", self.graph.nodes)
        self.assertIn("vpc-01", self.graph.nodes)
        self.assertIn("subnet-01", self.graph.nodes)

    def test_resource_relationships(self):
        self.assertTrue(
            self.graph.has_edge("i-web-01", "vpc-01")
        )

        self.assertTrue(
            self.graph.has_edge("i-web-01", "subnet-01")
        )

        self.assertTrue(
            self.graph.has_edge("db-prod-01", "vpc-01")
        )

    def test_topology_statistics(self):
        self.assertEqual(self.graph.number_of_nodes(), 6)
        self.assertEqual(self.graph.number_of_edges(), 5)


if __name__ == "__main__":
    unittest.main()