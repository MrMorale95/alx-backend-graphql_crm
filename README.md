# CRM Celery Beat Report Setup

This project generates a **weekly CRM report** (customers, orders, revenue) via Celery + Celery Beat and logs it to `/tmp/crm_report_log.txt`.

---

## Setup

### 1. Install Redis
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
