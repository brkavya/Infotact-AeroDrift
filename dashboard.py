from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

console = Console()

console.print(
    Panel(
        "AeroDrift Cloud Security Dashboard",
        title="AeroDrift"
    )
)

topology = Tree("☁ Cloud Topology")

internet = topology.add("🌐 Internet")
public_subnet = internet.add("📦 Public Subnet")
application = public_subnet.add("🖥 Application Server")
application.add("🗄 Private Database")

console.print(topology)


from rich.console import Console
from rich.tree import Tree

console = Console()

console.print("[bold cyan]AeroDrift Cloud Security Dashboard[/bold cyan]")

topology = Tree("☁ Cloud Topology")

internet = topology.add("🌐 Internet")
public_subnet = internet.add("📦 Public Subnet")
app_server = public_subnet.add("🖥 Application Server")
private_db = app_server.add("🗄 Private Database")

console.print(topology)

console.print("\n[bold]Status:[/bold] All resources available")
console.print("Internet: Online")
console.print("Public Subnet: Active")
console.print("Application Server: Running")
console.print("Private Database: Connected")

internet = topology.add("Internet")
subnet = internet.add("Public Subnet")
server = subnet.add("Application Server")
server.add("Private Database")

console.print(topology)
console.print("Status: All resources available")
console.print("Internet: Online")
console.print("Public Subnet: Active")
console.print("Application Server: Running")
console.print("Private Database: Connected")

console.print("\n[bold cyan]Resource Status[/bold cyan]")

console.print("[green]✓ Internet: Online[/green]")
console.print("[green]✓ Public Subnet: Active[/green]")
console.print("[green]✓ Application Server: Running[/green]")
console.print("[green]✓ Private Database: Connected[/green]")