git clone https://github.com/adamsiwiec1/stocks_realtime.git && \
bash docker_install_linux.sh && \
cd stocks_realtime && \
bash volumes.sh && \
docker compose -f mark-compose.yml up -d
