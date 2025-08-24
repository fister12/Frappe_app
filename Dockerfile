# Multi-stage Dockerfile for AI Quality Checker Frappe App

# Builder Stage
FROM frappe/bench:latest AS builder
# Use /home/frappe for bench initialization to avoid permission issues
WORKDIR /home/frappe
# Install redis-server for bench init (use sudo for permissions)
USER root
RUN apt-get update && apt-get install -y redis-server
USER frappe
RUN bench init --frappe-branch version-15 frappe-bench
WORKDIR /home/frappe/frappe-bench
RUN bench get-app https://github.com/fister12/Frappe_app.git

# ----------- Production Stage -----------
FROM frappe/erpnext-worker:latest AS production
WORKDIR /home/frappe/frappe-bench/sites/apps

# Copy the app from builder
COPY --from=builder /home/frappe/frappe-bench/apps/ai_quality_checker ./ai_quality_checker

# Set environment variables (example)
ENV FRAPPE_SITE_NAME=site1.local
ENV AI_QUALITY_CHECKER=1

# Expose necessary ports
EXPOSE 8000

CMD ["/home/frappe/frappe-bench/env/bin/gunicorn", "-b", "0.0.0.0:8000", "frappe.app:application"]
