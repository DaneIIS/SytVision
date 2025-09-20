# ---- build stage ----
FROM node:22-alpine AS build
WORKDIR /app

# Install deps first (better caching)
COPY package*.json ./
RUN npm ci

# Copy the rest and build
COPY . .
# Optional: pass your API base URL at build time if your app needs it (Vite/React etc.)
#   docker build --build-arg VITE_API_BASE_URL=http://nvr:8000 ...
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
RUN npm run build

# ---- runtime (nginx) ----
FROM nginx:alpine
# Replace the default site and static content
RUN rm -rf /etc/nginx/conf.d/default.conf /usr/share/nginx/html/*
# Bring in our nginx config (see below)
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy the built static assets
COPY --from=build /app/dist /usr/share/nginx/html/
EXPOSE 80
# Optional healthcheck if you have a /health endpoint in your SPA (or just check index)
HEALTHCHECK --interval=30s --timeout=3s --retries=5 CMD wget -qO- http://localhost/ >/dev/null 2>&1 || exit 1
