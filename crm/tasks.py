import logging
from celery import shared_task
from django.utils import timezone
from graphene.test import Client
from crm.schema import schema  # assumes you have a schema.py with Query

LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    client = Client(schema)

    # Query totals
    query = """
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """

    executed = client.execute(query)
    data = executed.get("data", {})

    total_customers = data.get("totalCustomers", 0)
    total_orders = data.get("totalOrders", 0)
    total_revenue = data.get("totalRevenue", 0)

    # Format log
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

    # Write to file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    logging.info("CRM report generated and logged.")
    return log_entry
