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

console.print("Status: System initialized")
console.print("Cloud topology: Loading...")
console.print("Resources: Internet | Subnet | Database")
topology = Tree("Cloud Topology")
console.print("Resources: Internet | Subnet | Database")


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