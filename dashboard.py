import networkx as nx

from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.table import Table

console = Console()


# =========================================================
# AeroDrift Dashboard Header
# =========================================================

console.print(
    Panel(
        "[bold cyan]AeroDrift Cloud Security Dashboard[/bold cyan]\n"
        "[white]CloudOps & Graph Security Monitoring[/white]",
        title="AeroDrift",
        border_style="cyan"
    )
)


# =========================================================
# NetworkX Cloud Topology
# =========================================================

topology = nx.DiGraph()

# Add cloud resources
topology.add_nodes_from([
    "Internet",
    "VPC",
    "Subnet",
    "EC2",
    "Database"
])

# Connect resources
topology.add_edges_from([
    ("Internet", "VPC"),
    ("VPC", "Subnet"),
    ("Subnet", "EC2"),
    ("EC2", "Database")
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
    header_style="bold cyan"
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
    "Path",
    "Internet → VPC → Subnet → EC2 → Database"
)

console.print(topology_table)


# =========================================================
# Resource Summary
# =========================================================

console.print()

summary = Table(
    title="Resource Summary",
    show_header=True,
    header_style="bold cyan"
)

summary.add_column("Resource")
summary.add_column("Count")
summary.add_column("Status")

summary.add_row(
    "VPC",
    "1",
    "[green]✓ Active[/green]"
)

summary.add_row(
    "Subnet",
    "1",
    "[green]✓ Active[/green]"
)

summary.add_row(
    "EC2",
    "1",
    "[green]✓ Running[/green]"
)

summary.add_row(
    "Database",
    "1",
    "[green]✓ Connected[/green]"
)

summary.add_row(
    "S3 Buckets",
    "0",
    "[yellow]⚠ None[/yellow]"
)


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
    header_style="bold cyan"
)

table.add_column("Resource", style="bold")
table.add_column("Status")
table.add_column("Health")

# Resource status data
resource_status = {
    "Internet": ("Online", "Healthy"),
    "VPC": ("Active", "Healthy"),
    "Subnet": ("Active", "Healthy"),
    "EC2": ("Running", "Drifted"),
    "Database": ("Connected", "Healthy")
}

# Add resources to health table
for resource, (status, health) in resource_status.items():
    table.add_row(
        resource,
        status,
        get_health_status(health)
    )

console.print(table)
# Health Summary
healthy_count = sum(
    1 for status in resource_status.values()
    if status[1] == "Healthy"
)

drifted_count = sum(
    1 for status in resource_status.values()
    if status[1] == "Drifted"
)

console.print(
    Panel(
        f"[green]✓ Healthy Resources: {healthy_count}[/green]\n"
        f"[red]⚠ Drifted Resources: {drifted_count}[/red]",
        title="Health Summary",
        border_style="cyan"
    )
)
# Health Percentage
total_resources = len(resource_status)

health_percentage = (healthy_count / total_resources) * 100

console.print(
    Panel(
        f"[cyan]Health Score: {health_percentage:.0f}%[/cyan]",
        title="Overall Health",
        border_style="cyan"
    )
)
# =========================================================
# Health Assessment
# =========================================================

if health_percentage == 100:
    assessment = "[green]✓ System health is excellent[/green]"
elif health_percentage >= 80:
    assessment = "[yellow]⚠ System health is good with minor issues[/yellow]"
elif health_percentage >= 60:
    assessment = "[yellow]⚠ System health needs attention[/yellow]"
else:
    assessment = "[red]⚠ System health is critical[/red]"

console.print(
    Panel(
        assessment,
        title="Health Assessment",
        border_style="cyan"
    )
)

# =========================================================
# System Summary
# =========================================================

console.print()

console.print(
    Panel(
        "[green]✓ All resources are available[/green]\n"
        "[green]✓ Cloud topology loaded successfully[/green]\n"
        "[green]✓ NetworkX topology initialized successfully[/green]\n"
        "[green]✓ Security dashboard initialized[/green]",
        title="System Status",
        border_style="green"
    )
)


# =========================================================
# Monitoring
# =========================================================

console.print(
    Panel(
        "[bold green]AeroDrift monitoring is active[/bold green]\n"
        "[green]✓ Topology monitoring enabled[/green]\n"
        "[green]✓ Resource health monitoring enabled[/green]",
        title="Monitoring",
        border_style="green"
    )
)


# =========================================================
# Security Status
# =========================================================

console.print(
    Panel(
        "[green]✓ Firewall: Active[/green]\n"
        "[green]✓ Security Scan: Passed[/green]\n"
        "[green]✓ Access Control: Enabled[/green]\n"
        "[green]✓ Encryption: Enabled[/green]",
        title="Security Status",
        border_style="green"
    )
)
# =========================================================
# Dynamic Security Alerts
# =========================================================

failed_login_attempts = 0

if drifted_count > 0:
    threat_detection = "[red]⚠ Threat Detection: Attention Required[/red]"
    security_alerts = "[red]⚠ Security Alerts: Resource Drift Detected[/red]"
else:
    threat_detection = "[green]✓ Threat Detection: Clear[/green]"
    security_alerts = "[green]✓ Security Alerts: None[/green]"

# =========================================================
# Security Score
# =========================================================

security_checks = {
    "Firewall": True,
    "Security Scan": True,
    "Access Control": True,
    "Encryption": True
}

security_score = (
    sum(security_checks.values()) / len(security_checks)
) * 100

console.print(
    Panel(
        f"[cyan]Security Score: {security_score:.0f}%[/cyan]",
        title="Security Score",
        border_style="cyan"
    )
)
# =========================================================
# Dynamic Threat Detection
# =========================================================

if drifted_count == 0:
    threat_status = "[green]✓ Threat Detection: Clear[/green]"
    security_alert = "[green]✓ Security Alerts: None[/green]"
else:
    threat_status = "[red]⚠ Threat Detection: Attention Required[/red]"
    security_alert = "[red]⚠ Security Alerts: Resource Drift Detected[/red]"
# =========================================================
# Security Alerts
# =========================================================

console.print(
    Panel(
        "[yellow]⚠ Failed Login Attempts: 0[/yellow]\n"
        "[green]✓ Unauthorized Access: None[/green]\n"
        f"{threat_status}\n"
        f"{security_alert}",
        title="Security Alerts",
        border_style="yellow"
    )
)