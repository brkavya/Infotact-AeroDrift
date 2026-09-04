"""
AeroDrift End-to-End Demonstration Runner
Chains topology validation, drift detection, remediation, and reporting.
"""
from rich.console import Console
from rich.panel import Panel
import subprocess
import sys

console = Console()

def run_step(step_name: str, command: list):
    console.print(f"\n[bold cyan]>>> Executing: {step_name}[/bold cyan]")
    result = subprocess.run([sys.executable] + command, capture_output=False)
    if result.returncode != 0:
        console.print(f"[bold red]❌ {step_name} failed with exit code {result.returncode}[/bold red]")
        sys.exit(result.returncode)

def main():
    console.print(Panel("[bold green]Starting AeroDrift CloudOps Pipeline Demo[/bold green]", expand=False))
    
    # 1. Topology Engine
    run_step("Cloud Infrastructure Topology Mapping", ["topology.py"])
    
    # 2. Automated Remediation Engine
    run_step("Automated Configuration Drift Remediation", ["remediation.py"])
    
    # 3. Security & Resource Dashboard
    run_step("System Health & Incident Dashboard", ["dashboard.py"])
    
    # 4. Verification Tests
    run_step("Automated Unit Test Suite", ["-m", "pytest", "-v"])

    console.print(Panel("[bold green]✔ AeroDrift Full Pipeline Execution Successful[/bold green]", expand=False))

if __name__ == "__main__":
    main()