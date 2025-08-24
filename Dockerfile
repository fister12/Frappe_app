# Multi-stage Dockerfile for AI Quality Checker Frappe App

# Builder Stage
FROM frappe/bench:latest AS builder
WORKDIR /home/frappe
USER root
RUN apt-get update && apt-get install -y redis-server
USER frappe
RUN bench init --frappe-branch version-15 frappe-bench
WORKDIR /home/frappe/frappe-bench
# Copy your local app code instead of cloning from GitHub
COPY ./ai_quality_checker /home/frappe/frappe-bench/apps/ai_quality_checker

# ----------- Production Stage -----------
FROM frappe/erpnext-worker:latest AS production
WORKDIR /home/frappe/frappe-bench/sites/apps

# Copy the app from builder
COPY --from=builder /home/frappe/frappe-bench/apps/ai_quality_checker ./ai_quality_checker

# Set environment variables (example)
ENV FRAPPE_SITE_NAME=site1.local
ENV AI_QUALITY_CHECKER=1

EXPOSE 8000

CMD ["/home/frappe/frappe-bench/env/bin/gunicorn", "-b", "0.0.0.0:8000", "frappe.app:application"]