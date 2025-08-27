import os
from datetime import datetime
import requests

def log_crm_heartbeat():
    """Logs heartbeat and optionally queries GraphQL hello field."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_path = "/tmp/crm_heartbeat_log.txt"

    # Optional GraphQL check
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.ok:
            data = response.json()
            hello_value = data.get("data", {}).get("hello", "No hello")
            message = f"{timestamp} CRM is alive (GraphQL says: {hello_value})"
        else:
            message = f"{timestamp} CRM is alive (GraphQL unreachable)"
    except Exception:
        message = f"{timestamp} CRM is alive (GraphQL check failed)"

    # Append to log file
    with open(log_path, "a") as f:
        f.write(message + "\n")
