FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY services/dispatcher-routing-app /src/dispatcher
RUN mkdir -p /app
RUN BACKEND_PATH="/src/dispatcher/app/backend" ; ALT_BACKEND="/src/dispatcher/backend" ; \
    if [ -f "${BACKEND_PATH}/requirements.txt" ]; then \
        cp "${BACKEND_PATH}/requirements.txt" /app/requirements.txt ; \
    elif [ -f "${ALT_BACKEND}/requirements.txt" ]; then \
        cp "${ALT_BACKEND}/requirements.txt" /app/requirements.txt ; \
    else \
        echo "# placeholder requirements" > /app/requirements.txt ; \
    fi

RUN if [ -s /app/requirements.txt ]; then pip install --no-cache-dir -r /app/requirements.txt; fi

RUN (pip install --no-cache-dir -e /libs/bluefolder-api || echo "TODO: make bluefolder-api installable; falling back to PYTHONPATH") \
    && (pip install --no-cache-dir -e /libs/optimized-routing-extension || echo "TODO: make optimized-routing-extension installable; falling back to PYTHONPATH")

ENV PYTHONPATH="/app:/libs/bluefolder-api:/libs/optimized-routing-extension:${PYTHONPATH}"

RUN BACKEND_PATH="/src/dispatcher/app/backend" ; ALT_BACKEND="/src/dispatcher/backend" ; \
    if [ -d "${BACKEND_PATH}" ]; then \
        cp -a "${BACKEND_PATH}/." /app/ ; \
    elif [ -d "${ALT_BACKEND}" ]; then \
        cp -a "${ALT_BACKEND}/." /app/ ; \
    else \
        echo "warning: no backend sources found; container will serve empty directory" ; \
    fi

EXPOSE ${DISPATCHER_BACKEND_PORT:-8000}

CMD ["sh", "-c", "${DISPATCHER_BACKEND_CMD:-python -m http.server ${DISPATCHER_BACKEND_PORT:-8000}}"]
