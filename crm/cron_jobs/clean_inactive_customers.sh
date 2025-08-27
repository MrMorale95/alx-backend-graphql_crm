#!/bin/bash

# Navigate to project root (adjust if manage.py is in another path)
cd "$(dirname "$0")/../.."

# Run Django shell command to delete inactive customers
deleted_count=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")

# Log results with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $deleted_count\" >> /tmp/customer_cleanup_log.txt
