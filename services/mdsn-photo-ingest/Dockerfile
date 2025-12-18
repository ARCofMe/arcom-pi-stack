FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY services/mdsn-photo-ingest /src/mdsn
RUN mkdir -p /app

RUN if [ -f /src/mdsn/external/requirements.txt ]; then \
        cp /src/mdsn/external/requirements.txt /app/requirements.txt ; \
    else \
        cp /src/mdsn/requirements.txt /app/requirements.txt ; \
    fi
RUN pip install --no-cache-dir -r /app/requirements.txt && pip install --no-cache-dir gunicorn

# Attempt editable installs of shared libs; fall back to PYTHONPATH if metadata is missing.
RUN (pip install --no-cache-dir -e /libs/bluefolder-api || echo "TODO: ensure bluefolder-api is installable; falling back to PYTHONPATH") \
    && (pip install --no-cache-dir -e /libs/optimized-routing-extension || echo "TODO: ensure optimized-routing-extension is installable; falling back to PYTHONPATH")

ENV PYTHONPATH="/app:/libs/bluefolder-api:/libs/optimized-routing-extension:${PYTHONPATH}"

RUN if [ -d /src/mdsn/external ]; then \
        cp -a /src/mdsn/external/. /app/ ; \
    else \
        cp -a /src/mdsn/. /app/ ; \
    fi

RUN mkdir -p /data

EXPOSE 5055

COPY services/mdsn-photo-ingest/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${MDSN_PORT:-5055} --workers 1 --threads 2 app.main:app"]
