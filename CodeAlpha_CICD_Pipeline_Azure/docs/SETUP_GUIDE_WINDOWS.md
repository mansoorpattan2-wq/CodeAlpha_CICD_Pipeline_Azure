# Complete Setup Guide — Windows (PowerShell / VS Code)

Follow these steps **in order**. Every command is explained before you run it.
Run all commands in **PowerShell inside VS Code's terminal** (View → Terminal).

---

## PART A — Local Project Setup

### Step 1: Verify prerequisites are installed

```powershell
python --version
git --version
docker --version
az --version
```
**What this does:** confirms Python, Git, Docker, and Azure CLI are installed and on your PATH. If any command fails with "not recognized", reinstall that tool and restart VS Code.

📸 **Screenshot 00:** capture this terminal output showing all four version numbers.

---

### Step 2: Create the project folder and open it in VS Code

```powershell
mkdir CodeAlpha_CICD_Pipeline_Azure
cd CodeAlpha_CICD_Pipeline_Azure
code .
```
**What this does:** creates your project folder, moves into it, then `code .` opens the current folder in VS Code.

(Copy in all the files from this delivered project into this folder now.)

---

### Step 3: Create and activate a Python virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```
**What this does:** `venv` creates an isolated Python environment so this project's packages don't conflict with other Python projects on your machine. `activate` switches your terminal into that environment (you'll see `(venv)` appear in the prompt).

---

### Step 4: Install dependencies

```powershell
pip install -r app/requirements.txt
pip install -r app/requirements-dev.txt
```
**What this does:** installs Flask + gunicorn (production dependencies) and pytest (testing dependency) into your virtual environment.

---

### Step 5: Run the app locally

```powershell
python app/app.py
```
**What this does:** starts the Flask development server on port 8000. Open **http://localhost:8000** in your browser to confirm it works.

📸 **Screenshot 01:** browser showing the running app.

Press `CTRL + C` in the terminal to stop the server when done.

---

### Step 6: Run automated tests

```powershell
pytest tests/ -v
```
**What this does:** runs all test functions in `tests/test_app.py` and prints a pass/fail report. `-v` means verbose output (shows each test by name).

---

### Step 7: Build and run the Docker image locally

```powershell
docker build -t codealpha-cicd-app .
```
**What this does:** reads the `Dockerfile` and builds a container image named `codealpha-cicd-app`. The `.` means "use the current directory as build context."

📸 **Screenshot 02:** terminal showing `docker build` completing successfully.

```powershell
docker run -p 8000:8000 codealpha-cicd-app
```
**What this does:** starts a container from that image, mapping port 8000 on your machine to port 8000 inside the container. Visit http://localhost:8000 again — it should work identically to Step 5, proving the containerized version behaves the same.

Press `CTRL + C` to stop it.

---

## PART B — Push Code to GitHub

See **[`GIT_COMMANDS.md`](../GIT_COMMANDS.md)** for the full step-by-step Git/GitHub instructions with commit messages.

---

## PART C — Create Azure Resources

Log in first:

```powershell
az login
```
**What this does:** opens a browser window to authenticate the Azure CLI with your Azure account. All following `az` commands act on your subscription.

---

### Step 1: Create a Resource Group

```powershell
az group create --name CodeAlpha-RG --location eastus
```
**What this does:** a Resource Group is a logical container that holds all related Azure resources (ACR, App Service, etc.) together, so you can manage/delete them as one unit. `--location eastus` picks the Azure datacenter region.

---

### Step 2: Create an Azure Container Registry (ACR)

```powershell
az acr create --resource-group CodeAlpha-RG --name codealphaacr --sku Basic --admin-enabled true
```
**What this does:** creates a private Docker registry named `codealphaacr` (registry names must be globally unique — change it if taken) to store your built images. `--sku Basic` is the cheapest tier, fine for this project. `--admin-enabled true` allows simple username/password auth (used by the pipeline's service connection).

📸 **Screenshot 04a:** Azure Portal showing the new ACR resource.

---

### Step 3: Create an App Service Plan

```powershell
az appservice plan create --name CodeAlpha-Plan --resource-group CodeAlpha-RG --sku B1 --is-linux
```
**What this does:** an App Service Plan defines the compute (CPU/RAM/pricing tier) that will run your web app. `--sku B1` is a low-cost Basic tier. `--is-linux` is required because we're deploying a Linux container.

---

### Step 4: Create the Web App (App Service for Containers)

```powershell
az webapp create --resource-group CodeAlpha-RG --plan CodeAlpha-Plan --name codealpha-cicd-webapp --deployment-container-image-name codealphaacr.azurecr.io/codealpha-cicd-app:latest
```
**What this does:** creates the actual Web App resource (`codealpha-cicd-webapp` — must also be globally unique) and points it at a starting container image. The pipeline will update this image automatically on every deploy.

---

### Step 5: Tell App Service which port your app listens on

```powershell
az webapp config appsettings set --resource-group CodeAlpha-RG --name codealpha-cicd-webapp --settings WEBSITES_PORT=8000
```
**What this does:** by default App Service expects containers to listen on port 80. Our Dockerfile exposes port 8000, so this setting tells App Service to route traffic there instead. **This is the #1 cause of "container fails to start" errors — don't skip it.**

---

### Step 6: Connect ACR to App Service

```powershell
az webapp config container set --name codealpha-cicd-webapp --resource-group CodeAlpha-RG --docker-custom-image-name codealphaacr.azurecr.io/codealpha-cicd-app:latest --docker-registry-server-url https://codealphaacr.azurecr.io
```
**What this does:** gives the Web App permission and configuration to pull images from your ACR.

---

## PART D — Set Up Azure Pipelines (Azure DevOps)

1. Go to https://dev.azure.com/ and create a new **Organization** (if you don't have one) and a new **Project** (e.g. `CodeAlpha-CICD`).
2. In the project, go to **Pipelines → Create Pipeline**.
3. Choose **GitHub** as the source, authorize Azure DevOps to access your GitHub account, and select your `CodeAlpha_CICD_Pipeline_Azure` repository.
4. Azure DevOps will detect the `azure-pipelines.yml` file in your repo automatically — select **"Existing Azure Pipelines YAML file"** and confirm.
5. **Before running**, create two Service Connections (Project Settings → Service connections → New service connection):
   - **Docker Registry** connection → type "Azure Container Registry" → select `codealphaacr` → name it exactly `acr-service-connection` (matches `azure-pipelines.yml`).
   - **Azure Resource Manager** connection → select your subscription → name it exactly `azure-service-connection`.
6. Update the `variables` block at the top of `azure-pipelines.yml` in your repo if you used different names than the examples above (e.g. your own unique ACR/webapp name), then commit and push.
7. Click **Run**. Watch the Build stage, then the Deploy stage, turn green.

📸 **Screenshot 03:** pipeline run showing both stages succeeded.
📸 **Screenshot 06:** App Service → Deployment Center showing the successful deployment.

---

## PART E — Verify the Live App

```powershell
az webapp browse --name codealpha-cicd-webapp --resource-group CodeAlpha-RG
```
**What this does:** opens your live deployed app in the default browser at `https://codealpha-cicd-webapp.azurewebsites.net`.

📸 **Screenshot 05:** the live app running in the browser with its public Azure URL visible.

---

## PART F — Clean Up (avoid ongoing charges)

Once you've captured all screenshots and are done demoing:

```powershell
az group delete --name CodeAlpha-RG --yes --no-wait
```
**What this does:** deletes the entire Resource Group and everything inside it (ACR, App Service, Plan) in one command, stopping any further billing. `--no-wait` returns control to your terminal immediately instead of waiting for deletion to finish.
