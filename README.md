## Usage

1. [Install Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
    [Linux Instal](https://docs.docker.com/desktop/install/linux-install/)
2. Set your API key in `.env`
3. Create your bind mounts with the provided `volumes.sh` script.
4. Start the project with Docker Compose.
```
docker compose -f mark-compose.yml up -d
```
4. Tail the logs to check it is working
```
docker exec 7ab51632c9e7 tail -f /home/pyparser.log
```


## Twelvedata Notes


