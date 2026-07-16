"""
app.py
------
A small Flask web application used to demonstrate an end-to-end CI/CD
pipeline (GitHub -> Azure Pipelines -> Azure Container Registry -> Azure App Service).

Routes:
    GET /          -> Renders a simple home page showing app + build info
    GET /health     -> Health check endpoint (used by Azure App Service / load balancers)
    GET /api/info    -> Returns JSON with app version and environment (useful for testing)
"""

import os
from datetime import datetime, timezone
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Read from environment variables so the SAME container image can behave
# differently per environment (a core DevOps concept: "build once, configure per environment").
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")


@app.route("/")
def home():
    """Renders the home page with basic app + deployment info."""
    return render_template(
        "index.html",
        version=APP_VERSION,
        environment=ENVIRONMENT,
        server_time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    )


@app.route("/health")
def health():
    """
    Health check endpoint.
    Azure App Service / container orchestrators call this to confirm the
    container is alive and ready to serve traffic.
    """
    return jsonify(status="healthy"), 200


@app.route("/api/info")
def info():
    """Returns app metadata as JSON — handy for automated pipeline tests."""
    return jsonify(
        app_name="CodeAlpha CI/CD Demo App",
        version=APP_VERSION,
        environment=ENVIRONMENT,
    )


if __name__ == "__main__":
    # Only runs for local dev ("python app.py"). In the container, gunicorn
    # runs the app instead — see Dockerfile.
    app.run(host="0.0.0.0", port=8000, debug=True)
