# Troubleshooting Guide

## Local development

**"python is not recognized as an internal or external command"**
Python isn't on your PATH. Reinstall Python and check "Add Python to PATH" during setup, then restart VS Code/PowerShell.

**"cannot be loaded because running scripts is disabled on this system" (activating venv)**
PowerShell's execution policy is blocking script execution. Run once as your user:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Then retry `venv\Scripts\activate`.

**Port 8000 already in use**
Another process is using that port. Either stop it, or run on a different port:
```powershell
python app/app.py  # then edit app.run(port=8001) temporarily
```

---

## Docker

**"error during connect... docker daemon is not running"**
Docker Desktop isn't started. Open Docker Desktop from the Start menu and wait until it shows "Engine running", then retry.

**"WSL 2 installation is incomplete"**
Run `wsl --update` in PowerShell (as Administrator), restart your machine, then reopen Docker Desktop.

**Image builds but container exits immediately**
Check logs with `docker logs <container_id>`. Common cause: a typo in the `CMD` line of the Dockerfile, or a missing dependency in `requirements.txt`.

---

## Azure CLI

**"az: command not found" / not recognized**
Azure CLI isn't installed or PATH wasn't refreshed. Reinstall from https://aka.ms/installazurecliwindows and open a **new** terminal window.

**"The subscription is not registered to use namespace..."**
Run:
```powershell
az provider register --namespace Microsoft.Web
az provider register --namespace Microsoft.ContainerRegistry
```
This enables the Azure services your resource group needs.

---

## Azure Container Registry

**"unauthorized: authentication required" when pipeline pushes image**
The ACR service connection is misconfigured or `--admin-enabled` was not set to true when creating the registry. Re-check Step 2 in the setup guide, or regenerate the service connection in Azure DevOps.

**Registry name already taken**
ACR names must be globally unique across all of Azure. Pick a more unique name (e.g. add your initials/numbers) and update it everywhere: `az acr create`, `azure-pipelines.yml` variables, and the App Service container settings.

---

## Azure App Service

**Container deploys but the site shows "Application Error" / doesn't load**
99% of the time this is the port mismatch. Confirm:
```powershell
az webapp config appsettings list --name codealpha-cicd-webapp --resource-group CodeAlpha-RG
```
and verify `WEBSITES_PORT=8000` is present (see Setup Guide Part C, Step 5).

**App shows an old version after deployment**
App Service can cache the container. Restart it:
```powershell
az webapp restart --name codealpha-cicd-webapp --resource-group CodeAlpha-RG
```

---

## Azure Pipelines

**Pipeline stuck "Waiting for an agent"**
Free Microsoft-hosted parallelism grants sometimes need manual activation for new organizations. Go to the pipeline's failed run message — it usually links directly to a Microsoft form to request free parallelism (takes ~2 business days) — or use a self-hosted agent in the meantime.

**"##[error]No hosted parallelism has been purchased or granted"**
Same cause as above — request free tier grant via the link Azure DevOps provides in the error message.

**Docker@2 task fails with "unable to resolve service connection"**
The service connection name in `azure-pipelines.yml` (`dockerRegistryServiceConnection` / `azureSubscription`) must **exactly** match the name you gave it in Project Settings → Service connections. Names are case-sensitive.

**Deploy stage skipped**
Check the Build stage actually succeeded — the Deploy stage only runs `condition: succeeded()`. Click into the Build stage logs to find the real failure.

---

## Git / GitHub

**"fatal: remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/<your-username>/CodeAlpha_CICD_Pipeline_Azure.git
```

**"Updates were rejected because the remote contains work that you do not have locally"**
Someone (or GitHub itself, e.g. auto-created README) added a commit you don't have. Run:
```powershell
git pull origin main --allow-unrelated-histories
```
then resolve any conflicts and push again.
