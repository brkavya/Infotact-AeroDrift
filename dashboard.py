from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel

console = Console()

# AeroDrift Dashboard Title
console.print(
    Panel(
        "AeroDrift Cloud Security Dashboard",
        title="AeroDrift"
    )
)

# Cloud Topology
topology = Tree("☁ Cloud Topology")

internet = topology.add("🌐 Internet")
public_subnet = internet.add("📦 Public Subnet")
application = public_subnet.add("🖥 Application Server")
application.add("🗄 Private Database")

console.print(topology)

# Resource Health
console.print()
console.print("[bold cyan]Resource Health[/bold cyan]")

console.print("[green]✓ Internet: Online[/green]")
console.print("[green]✓ Public Subnet: Active[/green]")
console.print("[green]✓ Application Server: Running[/green]")
console.print("[green]✓ Private Database: Connected[/green]")