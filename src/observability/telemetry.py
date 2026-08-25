import os

from dotenv import load_dotenv
from opentelemetry import trace


load_dotenv()

_configured = False


def configure_telemetry() -> None:
    global _configured

    if _configured:
        return

    connection_string = os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )

    if not connection_string:
        return

    from azure.monitor.opentelemetry import (
        configure_azure_monitor,
    )

    configure_azure_monitor(
        connection_string=connection_string,
        enable_live_metrics=True,
    )

    _configured = True


def get_tracer(name: str):
    return trace.get_tracer(name)