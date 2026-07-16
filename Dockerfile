# ---------------------------------------------------------------------------
# Dockerfile — builds a lightweight, production-ready image for the Flask app
# ---------------------------------------------------------------------------

# Use an official slim Python base image (small size = faster pulls/deploys)
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
# (unbuffered logs show up immediately in Azure App Service's Log Stream)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy only the requirements file first — Docker caches this layer so
# dependencies are NOT reinstalled every time app code changes (best practice)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY app/ .

# Create a non-root user and switch to it (security best practice —
# never run containers as root in production)
RUN useradd --create-home appuser
USER appuser

# Azure App Service for Containers expects the app to listen on port 8000
# (we set WEBSITES_PORT=8000 as an App Setting during deployment)
EXPOSE 8000

# Use gunicorn (production WSGI server) instead of Flask's dev server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
