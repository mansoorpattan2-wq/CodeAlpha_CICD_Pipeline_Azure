# Git & GitHub — Step-by-Step Commands

Run these one at a time in the VS Code PowerShell terminal, from inside the project folder.

## 1. Create the GitHub repository first
Go to https://github.com/new and create a repository named exactly:
```
CodeAlpha_CICD_Pipeline_Azure
```
Leave it **empty** (do NOT initialize with a README, .gitignore, or license — we already have our own).

## 2. Initialize Git locally
```powershell
git init
```
**What this does:** turns the current folder into a Git repository (creates a hidden `.git` folder that tracks history).

```powershell
git branch -M main
```
**What this does:** ensures your default branch is named `main` (matches the trigger in `azure-pipelines.yml`).

## 3. Configure your identity (skip if already set globally)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 4. Stage and commit the project — suggested commit sequence

```powershell
git add app/ tests/ requirements.txt
git commit -m "feat: add Flask application and unit tests"
```

```powershell
git add Dockerfile .dockerignore
git commit -m "feat: add Dockerfile for containerized deployment"
```

```powershell
git add azure-pipelines.yml
git commit -m "ci: add Azure Pipelines CI/CD workflow (build, test, push, deploy)"
```

```powershell
git add .gitignore
git commit -m "chore: add .gitignore"
```

```powershell
git add README.md docs/ GIT_COMMANDS.md LINKEDIN_VIDEO_SCRIPT.md
git commit -m "docs: add README, setup guide, troubleshooting and video script"
```

(If you'd rather commit everything in one go, that's fine too:)
```powershell
git add .
git commit -m "feat: initial commit - CI/CD pipeline project for CodeAlpha internship"
```

## 5. Connect to GitHub and push
```powershell
git remote add origin https://github.com/<your-username>/CodeAlpha_CICD_Pipeline_Azure.git
git push -u origin main
```
**What this does:** `remote add` links your local repo to the GitHub repo URL. `push -u origin main` uploads your commits and sets `origin/main` as the default upstream branch for future `git push` commands.

You'll be prompted to sign in to GitHub the first time (browser popup or a Personal Access Token).

## 6. Future changes
```powershell
git add .
git commit -m "fix: <describe your change>"
git push
```
Every push to `main` automatically triggers the Azure Pipeline.

## Good commit message examples for this project
- `feat: add health check endpoint`
- `fix: correct WEBSITES_PORT mismatch causing container startup failure`
- `ci: update pipeline to publish test results`
- `docs: update README with live app URL`
- `refactor: extract environment config into separate module`
- `test: add test coverage for /api/info endpoint`
