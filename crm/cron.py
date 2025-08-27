import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Logs heartbeat and queries GraphQL hello field to verify endpoint is responsive."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_path = "/tmp/crm_heartbeat_log.txt"

    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Query the hello field
    try:
        query = gql("{ hello }")
        result = client.execute(query)
        hello_value = result.get("hello", "No hello response")
        message = f"{timestamp} CRM is alive (GraphQL says: {hello_value})"
    except Exception:
        message = f"{timestamp} CRM is alive (GraphQL check failed)"

    # Append to log file
    with open(log_path, "a") as f:
        f.write(message + "\n")
