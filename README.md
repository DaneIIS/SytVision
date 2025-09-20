## 0. Preflight Check

``` bash
# ./nvr/ (where docker-compose.yml lives)
docker compose config       # validates compose
```

✅ Should print the resolved config without errors.

------------------------------------------------------------------------

## 1. Clean Build + Start

``` bash
docker compose build --no-cache --progress=plain
docker compose up -d
docker compose ps
```

✅ Both `nvr` and `frontend` should be "running".

------------------------------------------------------------------------

## 2. Backend (nvr) Basic Checks

``` bash
# Tail logs for obvious startup errors
docker compose logs -f nvr | sed -n '1,120p'

# Try a few likely endpoints
curl -sS http://localhost:8000/health || true
curl -sS http://localhost:8000/      || true
curl -sSI http://localhost:8000/     || true
```

✅ Look for 200/OK (or a sensible JSON/HTML response).

------------------------------------------------------------------------

## 3. Backend Python Dependencies

Verify that heavy libs like **cv2** and **dlib** load:

``` bash
docker compose exec nvr python - <<'PY'
import sys
print("Python:", sys.version.split()[0])
for mod in ("cv2","dlib","sklearn","scipy","PIL","gi","psycopg2","ultralytics"):
    try:
        m = __import__(mod)
        v = getattr(m, "__version__", "ok")
        print(f"{mod}: {v}")
    except Exception as e:
        print(f"{mod}: ERROR -> {e.__class__.__name__}: {e}")
PY
```

------------------------------------------------------------------------

## 4. Frontend (nginx) Check

``` bash
curl -sSI http://localhost:8080 | sed -n '1,6p'
curl -sS  http://localhost:8080 | head -n 20
```

✅ Expect `HTTP/1.1 200 OK` and some HTML.

------------------------------------------------------------------------

## 5. Frontend ↔︎ Backend Network Path

If your `nginx.conf` proxies `/api/` to `nvr:8000`:

``` bash
# From host
curl -sSI http://localhost:8080/api/ | sed -n '1,10p'

# From inside frontend
docker compose exec frontend sh -lc 'wget -qSO- http://nvr:8000/ 2>&1 | head -n 10'
```

✅ Should not be `502`/`504`. If it is, check nginx upstream config and
service names.

------------------------------------------------------------------------

## 6. Volume Mounts

``` bash
docker compose exec nvr sh -lc 'echo "hello" > /recordings/smoke.txt && ls -l /recordings/smoke.txt'
ls -l ./nvr/storage/smoke.txt
```

✅ File must exist in both places.

------------------------------------------------------------------------

## 7. Healthcheck (Optional)

``` bash
docker inspect --format='{{json .State.Health}}' $(docker compose ps -q nvr) | jq .
```

✅ `Status` should be `healthy`.

------------------------------------------------------------------------

## 8. Frontend Build Artifacts

``` bash
docker compose exec frontend sh -lc 'ls -lh /usr/share/nginx/html | head'
```

✅ Should include `index.html` and static assets.

------------------------------------------------------------------------

## 9. Cleanup (Optional)

``` bash
docker compose down -v
docker builder prune -f
```

------------------------------------------------------------------------

## ✅ Success Criteria

-   `docker compose ps` shows both containers **running**
-   Frontend reachable at <http://localhost:8080>
-   Backend reachable at <http://localhost:8000>
-   `/api/` proxy path works
-   Python import test succeeds for `cv2`, `dlib`, etc.
-   Host ↔︎ container volumes sync correctly
