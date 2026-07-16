# LinkedIn Demo Video Script (3–5 minutes)

Record your screen (VS Code + browser + Azure Portal) while speaking this. Aim for a natural, confident tone — not word-for-word reading.

---

### 1. Introduction (30 seconds)

> "Hi everyone, I'm Mansoor, a Computer Science undergrad and DevOps Intern at CodeAlpha. In this video, I'm walking through a project I built: a complete CI/CD pipeline that automatically builds, tests, and deploys a web application to the cloud every time I push code to GitHub — using Azure Pipelines, Azure Container Registry, and Azure App Service."

---

### 2. Problem Statement (30–45 seconds)

> "In real software teams, manually building and deploying an app every time there's a code change is slow and risky — it's easy to forget a step or deploy untested code. The goal of this project was to remove all of that manual work: push code once, and let automation handle testing, packaging it into a container, and getting it live — reliably, every single time."

*(Show the architecture diagram from the README on screen here.)*

---

### 3. Implementation (90–120 seconds)

> "Let me walk through how it's built."

- "The app itself is a simple Flask web application — nothing fancy, because the focus here is the pipeline, not the app." *(Show `app.py` briefly.)*
- "I containerized it with Docker — this Dockerfile installs dependencies, runs the app as a non-root user for security, and exposes it on port 8000." *(Show `Dockerfile`.)*
- "I wrote automated unit tests with pytest that check the home page, the health endpoint, and the info API — these run as a gate in the pipeline, so broken code never gets deployed." *(Show `test_app.py`.)*
- "The core of the project is this `azure-pipelines.yml` file. It has two stages: Build — which installs dependencies, runs the tests, and if they pass, builds the Docker image and pushes it to Azure Container Registry. And Deploy — which takes that exact image and deploys it to Azure App Service." *(Scroll through the YAML briefly, pointing at the two stages.)*
- "Everything is version-controlled in GitHub, and Azure Pipelines is connected directly to my repo, so any push to `main` triggers this automatically."

---

### 4. Demo (60–90 seconds)

> "Let me show it actually running."

- Make a small visible change (e.g., edit the HTML text or version number).
- `git add . / git commit -m "demo: update version" / git push`
- Switch to Azure DevOps → show the pipeline triggering automatically.
- Show the Build stage going green, then Deploy stage going green.
- Switch to the browser, refresh the live `*.azurewebsites.net` URL, and show your change is now live.

> "And that's it — from a single git push, my code was tested, containerized, pushed to Azure Container Registry, and deployed live, with zero manual steps."

---

### 5. Learning Outcomes (30–45 seconds)

> "Through this project I learned how to write multi-stage YAML pipelines, how to configure Azure Container Registry and App Service for containers, how to properly wire up service connections and troubleshoot real deployment issues like port mismatches, and — maybe most importantly — how automated testing gates prevent broken code from ever reaching production. This mirrors exactly how real DevOps teams ship software, and I'm excited to keep building on it. Thanks for watching — the full source code is on my GitHub, linked below."

---

## Recording tips
- Keep browser tabs pre-arranged: VS Code, GitHub repo, Azure DevOps pipeline, Azure Portal, live app — so you can switch smoothly without searching.
- Zoom in on your code editor font size (Ctrl + `+` in VS Code) so text is readable on LinkedIn's video player.
- Trim dead air where the pipeline is just running — you can speed up that portion in editing or talk over it.
