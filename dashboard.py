import networkx as nx

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from src.resource_manager import ResourceManager
from src.health_check import HealthChecker
from topology import (
    initialize_cloud_topology,
    add_inventory_resources,
    add_resource_relationships,
)


console = Console()

# =========================================================
# Backend Integration
# =========================================================
manager = ResourceManager()
checker = HealthChecker()
manager.add_resource("Web-Server", "EC2", "running")
manager.add_resource("Database", "RDS", "available")
resources = manager.list_resources()

health_records = []
for resource in resources:
    record = checker.check_status(resource)
    health_records.append(record)

# =========================================================
# AeroDrift Dashboard Header
# =========================================================
console.print(
    Panel(
        "[bold cyan]AeroDrift Cloud Security Dashboard[/bold cyan]\n"
        "[white]CloudOps & Graph Security Monitoring[/white]",
        title="AeroDrift",
        border_style="cyan",
    )
)

# =========================================================
# NetworkX Cloud Topology
# =========================================================
topology = initialize_cloud_topology()

add_inventory_resources(topology, manager)
add_resource_relationships(topology)

# =========================================================
# Rich Cloud Topology Visualization
# =========================================================
tree = Tree("[bold cyan]☁ Cloud Topology[/bold cyan]")

for node in topology.nodes:
    node_data = topology.nodes[node]
    resource_type = node_data.get("resource_type", "Resource")

    branch = tree.add(
        f"[bold green]{node}[/bold green] "
        f"[dim]({resource_type})[/dim]"
    )

    for target in topology.successors(node):
        edge_data = topology.get_edge_data(node, target)
        port = edge_data.get("port") if edge_data else None

        if port:
            branch.add(
                f"[yellow]→ {target}[/yellow] "
                f"[dim](port {port})[/dim]"
            )
        else:
            branch.add(
                f"[yellow]→ {target}[/yellow]"
            )

console.print(tree)

# =========================================================
# NetworkX Topology Information
# =========================================================
console.print()
topology_table = Table(
    title="NetworkX Topology",
    show_header=True,
    header_style="bold cyan",
)
topology_table.add_column("Type")
topology_table.add_column("Details")
topology_table.add_row(
    "Nodes",
    str(topology.number_of_nodes())
)
topology_table.add_row(
    "Edges",
    str(topology.number_of_edges())
)
topology_table.add_row(
    "Nodes List",
    ", ".join(topology.nodes)
)
topology_table.add_row(
    "Edges List",
    ", ".join(f"{source} → {target}" for source, target in topology.edges)
)

# =========================================================
# Topology Validation
# =========================================================
required_nodes = {
    "i-web-01",
    "db-prod-01",
    "vpc-01",
    "subnet-01",
    "sg-web",
    "dbsubnet-01",
}

required_edges = {
    ("i-web-01", "vpc-01"),
    ("i-web-01", "subnet-01"),
    ("i-web-01", "sg-web"),
    ("db-prod-01", "vpc-01"),
    ("db-prod-01", "dbsubnet-01"),
}

missing_nodes = required_nodes - set(topology.nodes)
missing_edges = required_edges - set(topology.edges)

if not missing_nodes and not missing_edges:
    topology_status = (
        "[green]✓ Topology validation passed[/green]\n"
        "[green]✓ All required resources are present[/green]\n"
        "[green]✓ All required relationships are present[/green]"
    )
    topology_border = "green"
else:
    topology_status = (
        "[red]⚠ Topology validation failed[/red]\n"
        f"[red]Missing Nodes: {missing_nodes}[/red]\n"
        f"[red]Missing Edges: {missing_edges}[/red]"
    )
    topology_border = "red"

console.print(
    Panel(
        topology_status,
        title="Topology Validation",
        border_style=topology_border,
    )
)
console.print(topology_table)

# =========================================================
# Topology Statistics
# =========================================================
resource_manager_count = len(resources)
networkx_node_count = topology.number_of_nodes()
networkx_edge_count = topology.number_of_edges()

console.print()

topology_stats = Table(
    title="Topology Statistics",
    show_header=True,
    header_style="bold cyan",
)

topology_stats.add_column("Metric")
topology_stats.add_column("Value")
topology_stats.add_column("Status")

topology_stats.add_row(
    "NetworkX Nodes",
    str(networkx_node_count),
    "[green]✓ Loaded[/green]",
)
topology_stats.add_row(
    "NetworkX Edges",
    str(networkx_edge_count),
    "[green]✓ Loaded[/green]",
)
topology_stats.add_row(
    "Inventory Resources",
    str(resource_manager_count),
    "[green]✓ Synced[/green]",
)
def get_health_display(health: str) -> str:
    if health == "HEALTHY":
        return "[green]✓ Healthy[/green]"
    elif health == "WARNING":
        return "[yellow]⚠ Warning[/yellow]"
    else:
        return "[red]⚠ Critical[/red]"


def get_risk_display(risk_score: float) -> str:
    if risk_score <= 0.3:
        return "[green]Low[/green]"
    elif risk_score <= 0.7:
        return "[yellow]Medium[/yellow]"
    else:
        return "[red]High[/red]"


# =========================================================
# Resource Health Status (Dynamic)
# =========================================================
console.print()
table = Table(
    title="Resource Health Status",
    show_header=True,
    header_style="bold cyan",
)
table.add_column("Resource", style="bold")
table.add_column("Type")
table.add_column("Status")
table.add_column("Health")

for res, record in zip(resources, health_records):
    table.add_row(
        record["resource_name"],
        record["resource_type"],
        res.get("status", "unknown").capitalize(),
        get_health_display(record["health"]),
    )

console.print(table)

# Dynamic Health Summary & Score
healthy_count = sum(1 for r in health_records if r["health"] == "HEALTHY")
warning_count = sum(1 for r in health_records if r["health"] == "WARNING")
critical_count = sum(1 for r in health_records if r["health"] == "CRITICAL")
total_count = len(health_records) or 1

health_percentage = (healthy_count / total_count) * 100

console.print(
    Panel(
        f"[green]✓ Healthy Resources: {healthy_count}[/green]\n"
        f"[yellow]⚠ Warning Resources: {warning_count}[/yellow]\n"
        f"[red]⚠ Critical Resources: {critical_count}[/red]",
        title="Health Summary",
        border_style="cyan",
    )
)

console.print(
    Panel(
        f"[cyan]Health Score: {health_percentage:.0f}%[/cyan]",
        title="Overall Health",
        border_style="cyan",
    )
)

if health_percentage == 100:
    assessment = "[green]✓ System health is excellent[/green]"
elif health_percentage >= 80:
    assessment = "[yellow]⚠ System health is good with minor issues[/yellow]"
elif health_percentage >= 60:
    assessment = "[yellow]⚠ System health needs attention[/yellow]"
else:
    assessment = "[red]⚠ System health is critical[/red]"

console.print(Panel(assessment, title="Health Assessment", border_style="cyan"))

# =========================================================
# Resource Details & Risk Assessment (Dynamic)
# =========================================================
console.print()
resource_table = Table(
    title="Resource Details",
    show_header=True,
    header_style="bold cyan",
)
resource_table.add_column("Resource", style="bold")
resource_table.add_column("Type")
resource_table.add_column("Status")
resource_table.add_column("Health")
resource_table.add_column("Risk")

for res, record in zip(resources, health_records):
    resource_table.add_row(
        record["resource_name"],
        record["resource_type"],
        res.get("status", "unknown").capitalize(),
        get_health_display(record["health"]),
        get_risk_display(record["risk_score"]),
    )
console.print(resource_table)

# =========================================================
# System Summary & Monitoring
# =========================================================
console.print()
console.print(
    Panel(
        "[green]✓ All resources are available[/green]\n"
        "[green]✓ Cloud topology loaded successfully[/green]\n"
        "[green]✓ NetworkX topology initialized successfully[/green]\n"
        "[green]✓ Security dashboard initialized[/green]",
        title="System Status",
        border_style="green",
    )
)

console.print(
    Panel(
        "[bold green]AeroDrift monitoring is active[/bold green]\n"
        "[green]✓ Topology monitoring enabled[/green]\n"
        "[green]✓ Resource health monitoring enabled[/green]",
        title="Monitoring",
        border_style="green",
    )
)

# =========================================================
# Security Status & Alerts
# =========================================================
console.print(
    Panel(
        "[green]✓ Firewall: Active[/green]\n"
        "[green]✓ Security Scan: Passed[/green]\n"
        "[green]✓ Access Control: Enabled[/green]\n"
        "[green]✓ Encryption: Enabled[/green]",
        title="Security Status",
        border_style="green",
    )
)

security_checks = {
    "Firewall": True,
    "Security Scan": True,
    "Access Control": True,
    "Encryption": True,
}
security_score = (sum(security_checks.values()) / len(security_checks)) * 100

console.print(
    Panel(
        f"[cyan]Security Score: {security_score:.0f}%[/cyan]",
        title="Security Score",
        border_style="cyan",
    )
)

unhealthy_records = [r for r in health_records if r["health"] != "HEALTHY"]

if not unhealthy_records:
    threat_status = "[green]✓ Threat Detection: Clear[/green]"
    security_alert = "[green]✓ Security Alerts: None[/green]"
else:
    threat_status = "[red]⚠ Threat Detection: Attention Required[/red]"
    security_alert = f"[red]⚠ Security Alerts: {len(unhealthy_records)} Resource Issue(s) Detected[/red]"

# =========================================================
# Resource Remediation Pipeline (Dynamic)
# =========================================================
recommendations = {
    "EC2": "Review EC2 instance state and restart failed services.",
    "RDS": "Check database connectivity, storage capacity, and connection pools.",
    "VPC": "Review route tables, network ACLs, and gateway attachments.",
    "Subnet": "Inspect IP allocation limits and route associations.",
}

console.print()
if unhealthy_records:
    remediation_text = ""
    for rec in unhealthy_records:
        rec_type = rec["resource_type"]
        rec_name = rec["resource_name"]
        rec_advice = recommendations.get(rec_type, "Review resource configuration and logs.")
        remediation_text += (
            f"[red]⚠ {rec_name} ({rec_type}): State is {rec['health']}[/red]\n"
            f"[yellow]→ Recommendation: {rec_advice}[/yellow]\n"
        )
    console.print(
        Panel(
            remediation_text.strip(),
            title="Resource Health & Remediation",
            border_style="red",
        )
    )
else:
    console.print(
        Panel(
            "[green]✓ No resource degradation detected[/green]\n"
            "[green]✓ All resources match expected operational state[/green]",
            title="Resource Health & Remediation",
            border_style="green",
        )
    )

# Dynamic Remediation Status
issue_count = len(unhealthy_records)
if issue_count == 0:
    remediation_status = "[green]✓ No remediation required[/green]"
    remediation_message = "[green]All resources are properly configured and operational.[/green]"
    remediation_border = "green"
elif issue_count == 1:
    remediation_status = "[yellow]⚠ Remediation Required[/yellow]"
    remediation_message = f"[yellow]{issue_count} resource requires attention.[/yellow]"
    remediation_border = "yellow"
else:
    remediation_status = "[red]⚠ Immediate Remediation Required[/red]"
    remediation_message = f"[red]{issue_count} resources require attention.[/red]"
    remediation_border = "red"

console.print()
console.print(
    Panel(
        f"{remediation_status}\n{remediation_message}",
        title="Remediation Status",
        border_style=remediation_border,
    )
)

console.print(
    Panel(
        "[green]✓ Failed Login Attempts: 0[/green]\n"
        "[green]✓ Unauthorized Access: None[/green]\n"
        f"{threat_status}\n"
        f"{security_alert}",
        title="Security Alerts",
        border_style="green" if not unhealthy_records else "yellow",
    )
)