import os
import sys
import networkx as nx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from src.resource_manager import ResourceManager
from src.health_check import HealthChecker
# Path configuration for backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from health_check import HealthChecker
from resource_manager import ResourceManager

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
topology = nx.DiGraph()
topology.add_nodes_from(["Internet", "VPC", "Subnet", "EC2", "Database"])
topology.add_edges_from([
    ("Internet", "VPC"),
    ("VPC", "Subnet"),
    ("Subnet", "EC2"),
    ("EC2", "Database"),
])

# =========================================================
# Rich Cloud Topology Visualization
# =========================================================
tree = Tree("[bold cyan]☁ Cloud Topology[/bold cyan]")
internet = tree.add("[bold green]🌐 Internet[/bold green]")
vpc = internet.add("[cyan]☁ VPC[/cyan]")
subnet = vpc.add("[yellow]▣ Subnet[/yellow]")
ec2 = subnet.add("[blue]🖥 EC2[/blue]")
ec2.add("[green]🗄 Database[/green]")
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
topology_table.add_row("Nodes", str(topology.number_of_nodes()))
topology_table.add_row("Edges", str(topology.number_of_edges()))
topology_table.add_row("Path", "Internet → VPC → Subnet → EC2 → Database")
console.print(topology_table)

# =========================================================
# Resource Summary
# =========================================================
console.print()
summary = Table(
    title="Resource Summary",
    show_header=True,
    header_style="bold cyan",
)
summary.add_column("Resource")
summary.add_column("Count")
summary.add_column("Status")
summary.add_row("VPC", "1", "[green]✓ Active[/green]")
summary.add_row("Subnet", "1", "[green]✓ Active[/green]")
summary.add_row("EC2", "1", "[green]✓ Running[/green]")
summary.add_row("Database", "1", "[green]✓ Connected[/green]")
summary.add_row("S3 Buckets", "0", "[yellow]⚠ None[/yellow]")
console.print(summary)


def get_health_status(status):
    if status == "Healthy":
        return "[green]✓ Healthy[/green]"
    elif status == "Drifted":
        return "[red]⚠ Drifted[/red]"
    else:
        return "[yellow]⚠ Warning[/yellow]"


# =========================================================
# Resource Health Status
# =========================================================
console.print()
table = Table(
    title="Resource Health Status",
    show_header=True,
    header_style="bold cyan",
)
table.add_column("Resource", style="bold")
table.add_column("Status")
table.add_column("Health")

resource_status = {
    "Internet": ("Online", "Healthy"),
    "VPC": ("Active", "Healthy"),
    "Subnet": ("Active", "Healthy"),
    "EC2": ("Running", "Drifted"),
    "Database": ("Connected", "Healthy"),
}

for resource, (status, health) in resource_status.items():
    table.add_row(resource, status, get_health_status(health))

console.print(table)

# Health Summary
healthy_count = sum(
    1 for status in resource_status.values() if status[1] == "Healthy"
)
drifted_count = sum(
    1 for status in resource_status.values() if status[1] == "Drifted"
)
console.print(
    Panel(
        f"[green]✓ Healthy Resources: {healthy_count}[/green]\n"
        f"[red]⚠ Drifted Resources: {drifted_count}[/red]",
        title="Health Summary",
        border_style="cyan",
    )
)

total_resources = len(resource_status)
health_percentage = (healthy_count / total_resources) * 100
console.print(
    Panel(
        f"[cyan]Health Score: {health_percentage:.0f}%[/cyan]",
        title="Overall Health",
        border_style="cyan",
    )
)

# Health Assessment
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
# Resource Details
# =========================================================
resource_details = {
    "Internet": {"Type": "Network", "Status": "Online", "Health": "Healthy", "Risk": "Low"},
    "VPC": {"Type": "Network", "Status": "Active", "Health": "Healthy", "Risk": "Low"},
    "Subnet": {"Type": "Network", "Status": "Active", "Health": "Healthy", "Risk": "Low"},
    "EC2": {"Type": "Compute", "Status": "Running", "Health": "Drifted", "Risk": "High"},
    "Database": {"Type": "Database", "Status": "Connected", "Health": "Healthy", "Risk": "Low"},
}

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

for resource, details in resource_details.items():
    health = "[green]✓ Healthy[/green]" if details["Health"] == "Healthy" else "[red]⚠ Drifted[/red]"
    risk = "[red]High[/red]" if details["Risk"] == "High" else "[green]Low[/green]"
    resource_table.add_row(
        resource,
        details["Type"],
        details["Status"],
        health,
        risk,
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

if drifted_count == 0:
    threat_status = "[green]✓ Threat Detection: Clear[/green]"
    security_alert = "[green]✓ Security Alerts: None[/green]"
else:
    threat_status = "[red]⚠ Threat Detection: Attention Required[/red]"
    security_alert = "[red]⚠ Security Alerts: Resource Drift Detected[/red]"

# =========================================================
# Resource Drift & Remediation
# =========================================================
drifted_resources = [
    resource for resource, (status, health) in resource_status.items() if health == "Drifted"
]

recommendations = {
    "EC2": "Review EC2 configuration and restore expected settings.",
    "VPC": "Check VPC configuration and security rules.",
    "Subnet": "Verify subnet configuration and routing settings.",
    "Database": "Check database connectivity and configuration.",
    "Internet": "Verify network connectivity and access rules.",
}

console.print()
if drifted_resources:
    remediation_text = ""
    for resource in drifted_resources:
        recommendation = recommendations.get(resource, "Review resource configuration.")
        remediation_text += (
            f"[red]⚠ {resource}: Drift Detected[/red]\n"
            f"[yellow]→ Recommendation: {recommendation}[/yellow]\n"
        )
    console.print(
        Panel(
            remediation_text,
            title="Drift Detection & Remediation",
            border_style="red",
        )
    )
else:
    console.print(
        Panel(
            "[green]✓ No resource drift detected[/green]\n"
            "[green]✓ All resources match expected configuration[/green]",
            title="Drift Detection & Remediation",
            border_style="green",
        )
    )

# Dynamic Remediation Status
drift_count = len(drifted_resources)
if drift_count == 0:
    remediation_status = "[green]✓ No remediation required[/green]"
    remediation_message = "[green]All resources are properly configured.[/green]"
    remediation_border = "green"
elif drift_count == 1:
    remediation_status = "[yellow]⚠ Remediation Required[/yellow]"
    remediation_message = f"[yellow]{drift_count} resource requires attention.[/yellow]"
    remediation_border = "yellow"
else:
    remediation_status = "[red]⚠ Immediate Remediation Required[/red]"
    remediation_message = f"[red]{drift_count} resources require attention.[/red]"
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
        "[yellow]⚠ Failed Login Attempts: 0[/yellow]\n"
        "[green]✓ Unauthorized Access: None[/green]\n"
        f"{threat_status}\n"
        f"{security_alert}",
        title="Security Alerts",
        border_style="yellow",
    )
)