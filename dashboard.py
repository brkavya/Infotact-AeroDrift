from rich.console import Console
from rich.panel import Panel

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