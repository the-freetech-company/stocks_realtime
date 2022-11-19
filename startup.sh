bash scripts/docker_install.sh -y && \
bash scripts/volumes.sh && \
bash scripts/portainer.sh && \  # portainer used for ease of monitoring
docker compose -f mark-compose.yml up -d