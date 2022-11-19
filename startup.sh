bash docker_install_linux.sh -y && \
bash volumes.sh && \
docker compose -f mark-compose.yml up -d
