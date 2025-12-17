FROM node:20-bullseye

WORKDIR /app

COPY services/dispatcher-routing-app /src/dispatcher

RUN FRONTEND_PATH="/src/dispatcher/app/frontend" ; ALT_FRONTEND="/src/dispatcher/frontend" ; \
    if [ -d "${FRONTEND_PATH}" ]; then \
        cp -a "${FRONTEND_PATH}/." /app/ ; \
    elif [ -d "${ALT_FRONTEND}" ]; then \
        cp -a "${ALT_FRONTEND}/." /app/ ; \
    else \
        echo 'console.log("dispatcher-frontend placeholder. Set DISPATCHER_FRONTEND_CMD to run real app.");' > /app/index.js ; \
        echo '{"name":"dispatcher-frontend-placeholder","version":"0.0.0"}' > /app/package.json ; \
        if [ -f "/src/dispatcher/frontend/placeholder-server.js" ]; then \
            cp /src/dispatcher/frontend/placeholder-server.js /app/placeholder-server.js ; \
        fi ; \
    fi

RUN if [ -f package.json ]; then npm install; else echo "No package.json found; running placeholder server."; fi

EXPOSE ${DISPATCHER_FRONTEND_PORT:-4173}

COPY services/dispatcher-routing-app/frontend/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["sh", "-c", "${DISPATCHER_FRONTEND_CMD:-npm run dev -- --host 0.0.0.0 --port ${DISPATCHER_FRONTEND_PORT:-4173}}"]
