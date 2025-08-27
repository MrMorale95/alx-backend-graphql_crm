from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    """Executes GraphQL mutation to restock low-stock products and logs updates."""
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_path = "/tmp/low_stock_updates_log.txt"  # correct file path

    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL mutation (call the mutation field 'updateLowStockProducts')
    mutation = gql("""
    mutation {
        updateLowStockProducts {
            updatedProducts {
                name
                stock
            }
            message
        }
    }
    """)

    try:
        result = client.execute(mutation)
        updated = result["updateLowStockProducts"]["updatedProducts"]

        with open(log_path, "a") as f:
            for product in updated:
                log_entry = f"{timestamp} - Product: {product['name']}, New Stock: {product['stock']}\n"
                f.write(log_entry)

    except Exception as e:
        with open(log_path, "a") as f:
            f.write(f"{timestamp} - Failed to update low-stock products: {e}\n")
