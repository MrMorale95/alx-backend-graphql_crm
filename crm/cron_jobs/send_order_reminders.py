#!/usr/bin/env python3
import sys
import os
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

def main():
    # Setup GraphQL transport
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Calculate cutoff date (7 days ago)
    cutoff_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # GraphQL query (adjust fields to your schema)
    query = gql("""
    query GetRecentOrders($cutoff: Date!) {
        orders(orderDate_Gte: $cutoff) {
            id
            customer {
                email
            }
            orderDate
            status
        }
    }
    """)

    # Execute query
    try:
        result = client.execute(query, variable_values={"cutoff": cutoff_date})
        orders = result.get("orders", [])

        log_path = "/tmp/order_reminders_log.txt"
        with open(log_path, "a") as f:
            for order in orders:
                log_entry = f"{datetime.now():%Y-%m-%d %H:%M:%S} - OrderID: {order['id']} - Email: {order['customer']['email']}\n"
                f.write(log_entry)

        print("Order reminders processed!")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
