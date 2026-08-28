import networkx as nx

from src.aws_loader import AWSLoader


def initialize_cloud_topology():
    """Create the NetworkX cloud topology from AWSLoader data."""

    cloud_graph = nx.DiGraph()

    loader = AWSLoader()
    resources = loader.load_resources()

    # Add AWS resources as nodes
    for resource in resources:
        cloud_graph.add_node(
            resource["id"],
            resource_type=resource["type"],
            metadata=resource["metadata"],
            region=resource["region"]
        )

    # Add relationships as edges
    for resource in resources:
        for rel in resource.get("relationships", []):
            target = rel["target"]

            cloud_graph.add_edge(
                resource["id"],
                target,
                relation=rel["type"]
            )

    return cloud_graph


def audit_security_drift(graph):
    """Check whether a path exists from Internet to the database."""

    try:
        path = nx.shortest_path(
            graph,
            source="Internet",
            target="Private_Database"
        )

        print(
            f"[!] SECURITY DRIFT DETECTED: "
            f"Path found from Internet to Database -> {path}"
        )

        return True

    except (nx.NetworkXNoPath, nx.NodeNotFound):
        print(
            "[✓] Cloud network is secure. "
            "No direct path from Internet to Database."
        )

        return False


def add_inventory_resources(graph, resource_manager):
    """Add ResourceManager inventory as nodes to the cloud graph."""

    for resource in resource_manager.list_resources():

        graph.add_node(
            resource["name"],
            resource_type=resource["type"],
            status=resource["status"],
            source="ResourceManager"
        )

    return graph


def add_resource_relationships(graph):
    """Add relationships between cloud resources."""

    relationships = [
        ("Internet", "Web-Server"),
        ("Web-Server", "Database"),
    ]

    for source, target in relationships:

        if source in graph.nodes and target in graph.nodes:

            graph.add_edge(
                source,
                target,
                relationship="connects"
            )

    return graph


if __name__ == "__main__":

    print("Initializing AeroDrift Cloud Topology Engine...")

    network_graph = initialize_cloud_topology()

    print("\nAWS Resources / Nodes:")
    for node, data in network_graph.nodes(data=True):
        print(node, data)

    print("\nResource Relationships / Edges:")
    for source, target, data in network_graph.edges(data=True):
        print(source, "->", target, data)

    print("\nTopology Statistics:")
    print("Total Nodes:", network_graph.number_of_nodes())
    print("Total Edges:", network_graph.number_of_edges())

    audit_security_drift(network_graph)