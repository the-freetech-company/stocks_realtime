bash docker_install_linux.sh && \
cd stocks_realtime && \
bash volumes.sh && \
docker compose -f mark-compose.yml up -d
