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
