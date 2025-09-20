FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System packages typically needed by:
# - dlib / face-recognition: build-essential, cmake, BLAS/OpenBLAS, X libs (some wheels link against libgl)
# - PyGObject: gobject-introspection headers, cairo, pkg-config
# - lxml (onvif-zeep): libxml2-dev, libxslt1-dev
# - psycopg2-binary: usually OK without libpq, but libpq5 ensures runtime compat
# - general: curl, git, pkg-config
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    pkg-config \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgirepository1.0-dev \
    gir1.2-glib-2.0 \
    libcairo2-dev \
    libxml2-dev \
    libxslt1-dev \
    libopenblas-dev \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps (prefer wheels where possible; install numpy first to speed up SciPy/Sklearn resolution)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --prefer-binary "numpy==1.26.4" \
 && python -m pip install --prefer-binary -r /app/requirements.txt

# Bring in the rest of the app
COPY . /app

EXPOSE 8000
# Adjust "main:app" to your actual ASGI app if different
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
