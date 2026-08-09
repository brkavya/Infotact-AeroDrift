import networkx as nx

def initialize_cloud_topology():
    cloud_graph = nx.DiGraph()
    cloud_graph.add_node("Internet", resource_type="Gateway", exposed_to_public=True)
    cloud_graph.add_node("Public_Subnet", resource_type="Subnet", exposed_to_public=True)
    cloud_graph.add_node("Private_Database", resource_type="Database", exposed_to_public=False)
    cloud_graph.add_edge("Internet", "Public_Subnet", port=443, open=True)
    cloud_graph.add_edge("Public_Subnet", "Private_Database", port=22, open=True)
    return cloud_graph

def audit_security_drift(graph):
    try:
        path = nx.shortest_path(graph, source="Internet", target="Private_Database")
        print(f"[!] SECURITY DRIFT DETECTED: Path found from Internet to Database -> {path}")
        return True
    except nx.NetworkXNoPath:
        print("[✓] Cloud network is secure. No direct path from Internet to Database.")
        return False

if __name__ == "__main__":
    print("Initializing AeroDrift Cloud Topology Engine...")
    network_graph = initialize_cloud_topology()
    print(f"Total Resources (Nodes): {list(network_graph.nodes)}")
    print(f"Network Pathways (Edges): {list(network_graph.edges)}")
    audit_security_drift(network_graph)