## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/DaneIIS/SytVision.git
cd SytVision

```

------------------------------------------------------------------------

## 2. Prepare local directories

``` bash
mkdir -p ./config ./storage ./segments ./snapshots ./thumbnails ./event_clips

```

------------------------------------------------------------------------

## 3. Build & start
Frontend: http://localhost:8080

``` bash
docker compose build --no-cache
docker compose up -d

```

# 4. Verify

``` bash
curl http://localhost:8000/health

```

------------------------------------------------------------------------

## Project Structure

```
SytVision/
├─ .github/ # GitHub workflows, issue/actions templates
├─ .vscode/ # VS Code configuration
├─ .devcontainer/ # Dev container config (if using Codespaces / Docker dev env)
├─ config/ # Project configuration files (env vars, settings, etc.)
├─ docker/ # Docker-related helper files (if any)
├─ docs/ # Documentation site / guides
├─ frontend/ # Frontend (SPA) built with Vite + React
│ ├─ public/ # Static assets (favicon, logo, etc.)
│ ├─ src/ # App source code
│ ├─ tests/ # Frontend tests (unit/e2e)
│ ├─ Dockerfile # Multi-stage build for frontend → nginx
│ ├─ nginx.conf # Nginx configuration for production/container
│ ├─ vite.config.ts # Vite build config & aliases
│ ├─ tsconfig.json # TypeScript config
│ ├─ tsconfig.node.json # Node / test environment config (if present)
│ ├─ package.json # Frontend dependencies & build scripts
│ └─ .dockerignore # files to ignore in Docker build context
├─ viseron/ # Main backend Python code
├─ scripts/ # Utility scripts (e.g. docs, setup, etc.)
├─ tests/ # Backend / integration tests
├─ rootfs/ # (if present) custom root filesystem additions
├─ .dockerignore # Global Docker ignore for project root
├─ docker-compose.yml # Compose file for orchestrating backend + frontend
├─ Dockerfile # Backend Dockerfile (Python + dependencies)
├─ requirements*.txt # Backend dependencies (production / dev / test)
├─ .pre-commit-config.yaml # Pre-commit hooks config
├─ .mypy.ini # MyPy / type-checking config
├─ .pylintrc # Pylint rules
├─ .flake8 / .isort.cfg # Formatting & import sorting config
├─ .gitignore # Files ignored by git
├─ LICENSE # Project license
└─ README.md # Project overview / build & run instructions
```
