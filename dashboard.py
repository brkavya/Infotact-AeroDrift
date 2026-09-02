from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from datetime import datetime
import os

from topology import initialize_cloud_topology


# =========================================================
# Console
# =========================================================

console = Console()


# =========================================================
# Dashboard Start Time
# =========================================================

execution_time = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)


# =========================================================
# Initialize Cloud Topology
# =========================================================

graph = initialize_cloud_topology()


# =========================================================
# Dashboard Overview
# =========================================================

console.print(
    Panel(
        "[bold cyan]AeroDrift Dashboard Summary[/bold cyan]\n"
        "Cloud security monitoring and topology overview\n\n"
        "[green]✓[/green] Network monitoring: Active\n"
        "[green]✓[/green] Resource monitoring: Active\n"
        "[green]✓[/green] Security monitoring: Active",
        title="Overview",
        border_style="cyan"
    )
)


# =========================================================
# Topology Information
# =========================================================

console.print(
    Panel(
        f"[cyan]Total Nodes:[/cyan] "
        f"{graph.number_of_nodes()}\n"

        f"[cyan]Total Relationships:[/cyan] "
        f"{graph.number_of_edges()}\n"

        "[green]Topology Status:[/green] Active",

        title="AeroDrift Cloud Topology",
        border_style="blue"
    )
)


# =========================================================
# Resource Table
# =========================================================

resource_table = Table(
    title="Cloud Resources",
    box=box.ROUNDED
)

resource_table.add_column(
    "Resource",
    style="cyan"
)

resource_table.add_column(
    "Type",
    style="magenta"
)

resource_table.add_column(
    "Status",
    style="green"
)


for node in graph.nodes:

    node_data = graph.nodes[node]

    resource_type = node_data.get(
        "type",
        "Unknown"
    )

    resource_table.add_row(
        str(node),
        str(resource_type),
        "Active"
    )


console.print(resource_table)


# =========================================================
# Topology Validation
# =========================================================

validation_messages = []


if graph.number_of_nodes() > 0:

    validation_messages.append(
        "[green]✓ Cloud resources detected[/green]"
    )


if graph.number_of_edges() > 0:

    validation_messages.append(
        "[green]✓ Resource relationships detected[/green]"
    )


console.print(
    Panel(
        "\n".join(validation_messages),
        title="Topology Validation",
        border_style="green"
    )
)


# =========================================================
# Resource Health Data
# =========================================================

# Resource monitoring information

resource_details = {

    "i-web-01": {
        "type": "Compute",
        "health": "Drifted",
        "risk": "High"
    },

    "db-prod-01": {
        "type": "Database",
        "health": "Healthy",
        "risk": "Low"
    },

    "vpc-01": {
        "type": "Network",
        "health": "Healthy",
        "risk": "Low"
    },

    "subnet-01": {
        "type": "Network",
        "health": "Healthy",
        "risk": "Low"
    }

}


# =========================================================
# Resource Health Table
# =========================================================

health_table = Table(
    title="Resource Health Status",
    box=box.ROUNDED
)


health_table.add_column(
    "Resource",
    style="cyan"
)

health_table.add_column(
    "Type",
    style="magenta"
)

health_table.add_column(
    "Health",
    style="yellow"
)

health_table.add_column(
    "Risk",
    style="red"
)


drifted_resources = []


for resource, details in resource_details.items():

    health = details["health"]
    risk = details["risk"]

    if health == "Drifted":

        drifted_resources.append(
            resource
        )

    health_table.add_row(
        resource,
        details["type"],
        health,
        risk
    )


console.print(health_table)


# =========================================================
# Health Summary
# =========================================================

total_resources = len(
    resource_details
)

drift_count = len(
    drifted_resources
)

healthy_count = (
    total_resources - drift_count
)


if total_resources > 0:

    health_percentage = int(
        (healthy_count / total_resources) * 100
    )

else:

    health_percentage = 100


console.print(
    Panel(
        f"[green]Healthy Resources:[/green] "
        f"{healthy_count}\n"

        f"[yellow]Drifted Resources:[/yellow] "
        f"{drift_count}\n"

        f"[cyan]Overall Health:[/cyan] "
        f"{health_percentage}%",

        title="Health Summary",
        border_style="green"
    )
)


# =========================================================
# Security Assessment
# =========================================================

if total_resources > 0:

    security_score = int(
        (healthy_count / total_resources) * 100
    )

else:

    security_score = 100


if security_score >= 80:

    security_status = (
        "[green]Secure[/green]"
    )

    security_border = "green"


elif security_score >= 50:

    security_status = (
        "[yellow]Moderate Risk[/yellow]"
    )

    security_border = "yellow"


else:

    security_status = (
        "[red]High Risk[/red]"
    )

    security_border = "red"


console.print(
    Panel(
        f"Security Score: "
        f"[bold]{security_score}%[/bold]\n"

        f"Status: {security_status}",

        title="Security Assessment",
        border_style=security_border
    )
)


# =========================================================
# Security Alerts
# =========================================================

if drift_count > 0:

    alert_message = (
        "[red]⚠ Security Alert: "
        "Resource Drift Detected[/red]\n\n"
    )

    for resource in drifted_resources:

        alert_message += (
            f"[yellow]Affected Resource:[/yellow] "
            f"{resource}\n"
        )


else:

    alert_message = (
        "[green]✓ No security alerts detected[/green]"
    )


console.print(
    Panel(
        alert_message,

        title="Security Alerts",

        border_style=(
            "red"
            if drift_count > 0
            else "green"
        )
    )
)


# =========================================================
# Structured Incident Report
# =========================================================

incident_reports = []


for index, resource in enumerate(
    drifted_resources,
    start=1
):

    details = resource_details[resource]

    incident = {

        "id": f"INC-{index:03d}",

        "resource": resource,

        "type": details["type"],

        "health": details["health"],

        "risk": details["risk"],

        "issue":
            "Resource configuration drift detected",

        "recommendation":
            "Review resource configuration and "
            "restore expected settings."

    }


    incident_reports.append(
        incident
    )


# =========================================================
# Display Incident Reports
# =========================================================

if incident_reports:

    for incident in incident_reports:

        incident_message = (

            f"[cyan]Incident ID:[/cyan] "
            f"{incident['id']}\n"

            f"[cyan]Resource:[/cyan] "
            f"{incident['resource']}\n"

            f"[cyan]Type:[/cyan] "
            f"{incident['type']}\n"

            f"[cyan]Health:[/cyan] "
            f"{incident['health']}\n"

            f"[red]Risk:[/red] "
            f"{incident['risk']}\n"

            f"[yellow]Issue:[/yellow] "
            f"{incident['issue']}\n"

            f"[green]Recommended Action:[/green] "
            f"{incident['recommendation']}"
        )


        console.print(
            Panel(
                incident_message,

                title="Incident Report",

                border_style="red"
            )
        )


else:

    console.print(
        Panel(
            "[green]✓ No incidents detected[/green]",

            title="Incident Report",

            border_style="green"
        )
    )


# =========================================================
# Week 4 Day 3 - Incident Summary
# =========================================================

total_incidents = len(
    incident_reports
)


high_risk_incidents = sum(

    1

    for incident in incident_reports

    if incident["risk"] == "High"

)


if total_incidents == 0:

    incident_status = (
        "[green]✓ No Incidents[/green]"
    )

    incident_border = "green"


else:

    incident_status = (
        "[red]⚠ Attention Required[/red]"
    )

    incident_border = "red"


console.print(
    Panel(

        f"[cyan]Total Incidents:[/cyan] "
        f"{total_incidents}\n"

        f"[red]High Risk Incidents:[/red] "
        f"{high_risk_incidents}\n"

        f"[yellow]Drifted Resources:[/yellow] "
        f"{drift_count}\n"

        f"Status: {incident_status}",

        title="Incident Summary",

        border_style=incident_border
    )
)


# =========================================================
# Automated Incident Logging
# =========================================================

log_directory = "logs"

log_file = os.path.join(
    log_directory,
    "incidents.log"
)


os.makedirs(
    log_directory,
    exist_ok=True
)


new_incidents_logged = 0


existing_logs = ""


if os.path.exists(log_file):

    with open(
        log_file,
        "r",
        encoding="utf-8"
    ) as file:

        existing_logs = file.read()


with open(
    log_file,
    "a",
    encoding="utf-8"
) as file:

    for incident in incident_reports:

        log_entry = (

            f"[{execution_time}] "

            f"Incident ID: {incident['id']} | "

            f"Resource: {incident['resource']} | "

            f"Type: {incident['type']} | "

            f"Health: {incident['health']} | "

            f"Risk: {incident['risk']} | "

            f"Issue: {incident['issue']} | "

            f"Recommendation: "
            f"{incident['recommendation']}\n"

        )


        # Prevent duplicate incident IDs
        # from being logged again

        if incident["id"] not in existing_logs:

            file.write(
                log_entry
            )

            new_incidents_logged += 1


# =========================================================
# Incident Logging Status
# =========================================================

console.print(
    Panel(

        "[green]✓ Incident report logging enabled[/green]\n"

        f"Log File: {log_file}\n"

        f"Detected Incidents: "
        f"{total_incidents}\n"

        f"New Incidents Logged This Run: "
        f"{new_incidents_logged}",

        title="Incident Logging",

        border_style="green"
    )
)


# =========================================================
# Report Information
# =========================================================

console.print(
    Panel(

        f"[cyan]Report Generated:[/cyan] "
        f"{execution_time}\n"

        "[green]Monitoring Status:[/green] Active\n"

        "[yellow]Dashboard Version:[/yellow] "
        "Week 4 Day 3",

        title="Report Information",

        border_style="blue"
    )
)


# =========================================================
# System Complete
# =========================================================

console.print(
    Panel(

        "[green]✓ AeroDrift dashboard execution "
        "completed successfully[/green]",

        title="System Complete",

        border_style="green"
    )
)