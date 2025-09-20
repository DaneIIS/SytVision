
# Rebuild Frontend & Verify

This guide shows how to rebuild the **frontend** and verify the app is working via Docker Compose (and optionally via local dev server).

---

## Prerequisites
- Repo cloned and in project root (contains `docker-compose.yml`).
- Frontend code under `frontend/` with `Dockerfile` and `nginx.conf`.
- Backend service (`nvr`) running or available via Docker Compose.
- Optional: `SytVisionProvider` integrated in the entry file (so branding/context is loaded).

---

## Rebuild with Docker Compose (production image)

```bash
# From repo root
docker compose build --no-cache --progress=plain frontend
docker compose up -d frontend
```

### Verify
```bash
# Check container status
docker compose ps

# Check the UI responds
curl -I http://localhost:8080

# Verify API proxy (frontend -> backend at nvr:8000)
# If your backend exposes /health:
curl -sS http://localhost:8080/api/health

# View recent logs (frontend only)
docker compose logs --tail=100 frontend
```

If you changed `nginx.conf`, ensure the build ran again with `--no-cache`, or force a restart:
```bash
docker compose up -d --build frontend
```

---

## Local Dev (optional: Vite dev server)

```bash
cd frontend
npm ci           # or: pnpm i / yarn
npm run dev      # Vite dev server (http://localhost:5173 by default)
```

If your API calls expect `/api/*`, either run the backend separately or add a Vite proxy in `vite.config.ts`:

```ts
// vite.config.ts
export default defineConfig({
  // ...
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000", // backend
        changeOrigin: true,
        rewrite: (p) => p.replace(/^\/api/, ""),
      },
    },
  },
});
```

---

## Healthchecks (backend)

Your Compose should define a backend healthcheck (example):
```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -fsS http://localhost:8000/health || exit 1"]
  interval: 15s
  timeout: 3s
  retries: 10
```

`frontend` depends on the backend being healthy:
```yaml
frontend:
  depends_on:
    nvr:
      condition: service_healthy
```

---

## Common Gotchas

- **TypeScript error TS18003** (“No inputs were found”): ensure `frontend/src` exists and is copied in the Docker build; double‑check `frontend/.dockerignore` isn’t excluding `src/`.  
- **Proxy 502/504 via `/api/*`**: verify the backend is healthy and `nginx.conf` uses `proxy_pass http://nvr:8000/;` (note the trailing slash).  
- **Port conflicts**: if 8080 is in use, change `ports: ["8081:80"]` in `docker-compose.yml`.  
- **Cache busting**: use `--no-cache` when rebuilding if static assets or `nginx.conf` changed.  
- **Missing curl in container**: backend healthcheck requires `curl` installed in the backend image.

---

## Quick One-Liners

```bash
# Full rebuild of both services
docker compose build --no-cache --progress=plain && docker compose up -d

# Only frontend rebuild
docker compose build --no-cache frontend && docker compose up -d frontend

# Check endpoints
curl -I http://localhost:8080
curl -sS http://localhost:8080/api/health
```

---

## Success Criteria

- `docker compose ps` shows `frontend` and `nvr` **running** (nvr = healthy).
- `http://localhost:8080` returns your SPA (title shows "SytVision" if you set it).
- `http://localhost:8080/api/health` returns a healthy response from the backend.
- Frontend assets are current (reloaded after a rebuild).


# Frontend File Structure

```
frontend/
├─ public/                     # Static assets copied as-is
│  └─ favicon.svg
├─ src/                        # Application source
│  ├─ assets/                  # Images, fonts, misc. assets
│  ├─ components/              # Reusable UI components
│  ├─ hooks/                   # Custom React hooks
│  ├─ pages/                   # Route-level views/screens
│  ├─ lib/                     # Utilities, API clients, helpers
│  ├─ styles/                  # Global styles (CSS/Tailwind/etc.)
│  ├─ App.tsx                  # Root component
│  └─ main.tsx                 # React/Vite entrypoint
├─ tests/                      # (optional) unit/e2e tests
├─ nginx.conf                  # Nginx vhost (production container)
├─ Dockerfile                  # Multi-stage build (Node → Nginx)
├─ index.html                  # HTML shell (Vite)
├─ package.json                # Scripts & deps
├─ tsconfig.json               # TypeScript configuration
├─ tsconfig.node.json          # (optional) Node/Vitest config
├─ vite.config.ts              # Vite build config & path aliases
└─ .dockerignore               # Exclude node_modules/dist from build context
```
