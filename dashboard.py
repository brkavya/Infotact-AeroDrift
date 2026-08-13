from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.table import Table

console = Console()

# -----------------------------
# AeroDrift Dashboard Header
# -----------------------------
console.print(
    Panel(
        "[bold cyan]AeroDrift Cloud Security Dashboard[/bold cyan]\n"
        "[white]CloudOps & Graph Security Monitoring[/white]",
        title="AeroDrift",
        border_style="cyan"
    )
)

# -----------------------------
# Cloud Topology
# -----------------------------
topology = Tree("[bold cyan]☁ Cloud Topology[/bold cyan]")

internet = topology.add("[bold green]🌐 Internet[/bold green]")
public_subnet = internet.add("[yellow]▣ Public Subnet[/yellow]")
application = public_subnet.add("[blue]▣ Application Server[/blue]")
application.add("[green]▣ Private Database[/green]")

console.print(topology)

# -----------------------------
# Resource Health Status
# -----------------------------
console.print()

table = Table(
    title="Resource Health Status",
    show_header=True,
    header_style="bold cyan"
)

table.add_column("Resource", style="bold")
table.add_column("Status")
table.add_column("Health")

table.add_row(
    "Internet",
    "[green]Online[/green]",
    "[green]✓ Healthy[/green]"
)

table.add_row(
    "Public Subnet",
    "[green]Active[/green]",
    "[green]✓ Healthy[/green]"
)

table.add_row(
    "Application Server",
    "[green]Running[/green]",
    "[green]✓ Healthy[/green]"
)

table.add_row(
    "Private Database",
    "[green]Connected[/green]",
    "[green]✓ Healthy[/green]"
)

console.print(table)

# -----------------------------
# System Summary
# -----------------------------
console.print()

console.print(
    Panel(
        "[green]✓ All resources are available[/green]\n"
        "[green]✓ Cloud topology loaded successfully[/green]\n"
        "[green]✓ Security dashboard initialized[/green]",
        title="System Status",
        border_style="green"
    )
)