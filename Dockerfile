# Multi-stage Dockerfile for AI Quality Checker Frappe App

# ----------- Builder Stage -----------
FROM frappe/bench:latest AS builder
WORKDIR /workspace

# Clone the custom app from its repository (replace with your repo URL)
RUN bench get-app https://github.com/yourusername/ai_quality_checker.git

# ----------- Production Stage -----------
FROM frappe/erpnext-worker:v15 AS production
WORKDIR /home/frappe/frappe-bench/sites/apps

# Copy the app from builder
COPY --from=builder /workspace/apps/ai_quality_checker ./ai_quality_checker

# Set environment variables (example)
ENV FRAPPE_SITE_NAME=site1.local
ENV AI_QUALITY_CHECKER=1

# Expose necessary ports
EXPOSE 8000

CMD ["/home/frappe/frappe-bench/env/bin/gunicorn", "-b", "0.0.0.0:8000", "frappe.app:application"]
