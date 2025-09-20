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

``` bash
SytVision/
├── frontend/          # React/Vite + Nginx config
├── viseron/           # Python backend code
├── docker-compose.yml # Multi-service orchestration
├── Dockerfile         # Backend build (Python)
├── README.md
└── ...
