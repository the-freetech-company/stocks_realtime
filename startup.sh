chmod +x scripts/* && \
bash scripts/docker_install.sh -y && \
bash scripts/volumes.sh && \
bash scripts/portainer.sh && \  # portainer used for ease of monitoring
docker compose -f stocks-compose.yml up -d