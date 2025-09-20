FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Native deps for dlib/face-recognition, scipy/sklearn, PyGObject, lxml/zeep, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git curl pkg-config \
    libopenblas-dev \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 \
    libgirepository1.0-dev gir1.2-glib-2.0 libcairo2-dev \
    libxml2-dev libxslt1-dev \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps (numpy first helps wheels resolve quickly)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --prefer-binary "numpy==1.26.4" \
 && python -m pip install --prefer-binary -r /app/requirements.txt

# App source
COPY . /app

EXPOSE 8000

# Adjust module if different (e.g., app.main:app)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
