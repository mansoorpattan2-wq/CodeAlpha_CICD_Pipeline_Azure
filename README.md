# CodeAlpha_CICD_Pipeline_Azure

A complete, production-style **CI/CD pipeline** that automatically builds, tests, containerizes, and deploys a Flask web application whenever code is pushed to GitHub — using **Azure Pipelines**, **Azure Container Registry (ACR)**, and **Azure App Service**.

> Built as part of the **CodeAlpha DevOps Internship** program.

---

## 📌 Project Overview

Manually building, testing, and deploying software is slow and error-prone. This project solves that by automating the entire journey from `git push` to a live, running application on the internet — with zero manual steps in between.

**Pipeline flow:**

```
Developer pushes code to GitHub (main branch)
                │
                ▼
   Azure Pipelines is triggered automatically
                │
        ┌───────┴────────┐
        ▼                 ▼
  Stage 1: BUILD      Stage 2: DEPLOY
  - Install deps       - Pull image from ACR
  - Run unit tests      - Deploy to Azure
  - Build Docker image     App Service
  - Push image to ACR   - App goes live
        │                 │
        ▼                 ▼
  Azure Container    https://<app>.azurewebsites.net
    Registry (ACR)
```

---

## ✨ Features

- Fully automated CI/CD — no manual build or deploy steps
- Automated unit testing gate (bad code never reaches production)
- Dockerized application (runs identically everywhere)
- Immutable, traceable image tags (`Build.BuildId`) for every release
- Runs as a non-root user inside the container (security best practice)
- Health check endpoint (`/health`) for monitoring
- Environment-based configuration (build once, configure per environment)
- Clean separation of source code, tests, infra config, and docs

---

## 🛠️ Technologies Used

| Category            | Tool / Service              |
|----------------------|------------------------------|
| Language / Framework | Python 3.11, Flask            |
| Web server (prod)     | Gunicorn                     |
| Containerization      | Docker                        |
| CI/CD                 | Azure Pipelines (YAML)        |
| Image registry        | Azure Container Registry (ACR)|
| Hosting                | Azure App Service (Web App for Containers) |
| Version control        | Git & GitHub                  |
| Testing                | Pytest                        |

---

## 📁 Folder Structure

```
CodeAlpha_CICD_Pipeline_Azure/
│
├── app/                        # Application source code
│   ├── app.py                   # Flask application (routes: /, /health, /api/info)
│   ├── requirements.txt          # Production dependencies
│   ├── requirements-dev.txt       # Dev/test-only dependencies (pytest)
│   ├── templates/
│   │   └── index.html            # HTML page
│   └── static/
│       └── style.css             # Styling
│
├── tests/
│   └── test_app.py               # Automated unit tests
│
├── docs/
│   ├── SETUP_GUIDE_WINDOWS.md    # Full Windows setup walkthrough
│   ├── TROUBLESHOOTING.md        # Common errors & fixes
│   └── screenshots/               # Screenshot evidence (see checklist inside)
│
├── Dockerfile                    # Container build definition
├── .dockerignore
├── azure-pipelines.yml            # CI/CD pipeline definition
├── .gitignore
├── GIT_COMMANDS.md                 # Step-by-step Git/GitHub commands
├── LINKEDIN_VIDEO_SCRIPT.md         # 3–5 min demo video script
└── README.md                      # You are here
```

---

## ✅ Prerequisites

Install these before you begin (all free):

1. **Windows 10/11**
2. **VS Code** — https://code.visualstudio.com/
3. **Python 3.11+** — https://www.python.org/downloads/ (check "Add Python to PATH" during install)
4. **Git for Windows** — https://git-scm.com/download/win
5. **Docker Desktop** — https://www.docker.com/products/docker-desktop/ (requires WSL2, which the installer sets up for you)
6. **Azure CLI** — https://aka.ms/installazurecliwindows
7. A **free Azure account** — https://azure.microsoft.com/free/ (requires a card for identity verification; free tier resources used here cost very little/nothing if cleaned up after)
8. A **GitHub account** — https://github.com/
9. An **Azure DevOps organization** (free) — https://dev.azure.com/

---

## 🚀 Installation & Setup

Full, copy-pasteable, one-command-at-a-time instructions (including every Azure resource you need to create) are in:

👉 **[`docs/SETUP_GUIDE_WINDOWS.md`](docs/SETUP_GUIDE_WINDOWS.md)**

Short version:

```powershell
# 1. Clone your repo
git clone https://github.com/<your-username>/CodeAlpha_CICD_Pipeline_Azure.git
cd CodeAlpha_CICD_Pipeline_Azure

# 2. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r app/requirements.txt
pip install -r app/requirements-dev.txt

# 4. Run the app locally
python app/app.py
```

Then open **http://localhost:8000** in your browser.

---

## ▶️ Usage

**Run tests:**
```powershell
pytest tests/
```

**Build & run with Docker locally:**
```powershell
docker build -t codealpha-cicd-app .
docker run -p 8000:8000 codealpha-cicd-app
```

**Trigger the real pipeline:** simply push a commit to the `main` branch on GitHub. Azure Pipelines picks it up automatically (once connected — see setup guide) and runs the full build → test → containerize → deploy flow.

---

## 📸 Output

The deployed app shows the app version, environment, and live server time — proof that the container running in Azure is the exact one built by the pipeline.

| What to capture | Where |
|---|---|
| Local app running in browser | `docs/screenshots/01-local-app.png` |
| `docker build` success in terminal | `docs/screenshots/02-docker-build.png` |
| Azure Pipeline run — all green stages | `docs/screenshots/03-pipeline-success.png` |
| Image visible inside ACR (Azure Portal) | `docs/screenshots/04-acr-repository.png` |
| Live app running on `*.azurewebsites.net` | `docs/screenshots/05-live-app.png` |
| App Service "Deployment Center" showing last deploy | `docs/screenshots/06-deployment-center.png` |

(See `docs/screenshots/README.md` for the full checklist and exact steps to capture each one.)

---

## 🐞 Troubleshooting

Full list of common errors and fixes: **[`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)**

---

## 🔮 Future Enhancements

- Add a **staging** environment/slot with manual approval before production swap
- Integrate **SonarCloud** or similar for static code analysis in the Build stage
- Add **Azure Application Insights** for live monitoring and alerting
- Use **Azure Key Vault** for secrets instead of pipeline variables
- Add **Blue-Green deployment** via App Service deployment slots
- Add a **badge** in this README showing live pipeline build status

---

## 👤 Author

Built by Mansoor — B.Tech Computer Science, Narasaraopeta Engineering College — as part of the **CodeAlpha DevOps Internship**.

## 📄 License

This project is submitted for educational/internship purposes and is free to use as a learning reference.
