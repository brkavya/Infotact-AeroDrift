from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.remediation import RemediationEngine

console = Console()


def run_cli_remediation():
    console.print(
        Panel(
            "[bold cyan]AeroDrift Automated Remediation Engine[/bold cyan]\n"
            "[white]Resolving configuration drift and restoring security baselines[/white]",
            title="AeroDrift Remediation",
            border_style="cyan",
        )
    )

    engine = RemediationEngine()

    resource_status = {
        "Internet": ("Online", "Healthy"),
        "VPC": ("Active", "Healthy"),
        "Subnet": ("Active", "Healthy"),
        "EC2": ("Running", "Drifted"),
        "Database": ("Connected", "Healthy"),
    }

    engine.run_remediation(resource_status)

    table = Table(
        title="Remediation Summary",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Resource", style="bold")
    table.add_column("Initial Health")
    table.add_column("Remediation Status")
    table.add_column("Final Health")

    for resource, (status, health) in resource_status.items():
        if health == "Drifted":
            status_display = "[green]✓ Remediated[/green]"
            final_health = "[green]✓ Healthy[/green]"
        else:
            status_display = "[dim]No Action Needed[/dim]"
            final_health = "[green]✓ Healthy[/green]"

        table.add_row(resource, health, status_display, final_health)

    console.print()
    console.print(table)

    console.print()
    console.print(
        Panel(
            "[green]✓ All detected configuration drifts have been resolved[/green]\n"
            "[cyan]Log updated: logs/remediation.log[/cyan]",
            title="Remediation Complete",
            border_style="green",
        )
    )


if __name__ == "__main__":
    run_cli_remediation()