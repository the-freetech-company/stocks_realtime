## Usage (Linux Server)

1. Log into your server.
```
ssh user@myserver
```
2. Clone the repository and `cd` into it.
```
git clone https://github.com/adamsiwiec1/stocks_realtime.git
cd stocks_realtime
```
3. Create an `.env` file (`stocks_realtime/.env`) to store secrets and variables.
```
API_KEY=twelvedata_key
MONGO_USER=mongo
MONGO_PASSWORD=mongo
MONGO_INITDB_ROOT_USERNAME=mongo
MONGO_INITDB_ROOT_PASSWORD=mongo
MONGO_PUBLIC_IP=192.168.1.38
MONGO_PORT=27017
SYMBOLS=["0xBTC/BTC", "ETH/BTC", "BTC/USD", "GRT/BTC", "XRP/BTC", "DOGE/BTC", "BNB/BTC"]
``` 
4. Give `startup.sh` execute permission and run the script.
```
chmod +x startup.sh
./startup.sh
```
5. Ensure the containers have started and obtain your pyparser container id. (ex below: ce9d45181c95)
```
root@twelvedata:/home/mark/stocks_realtime# docker ps
CONTAINER ID   IMAGE                    COMMAND                   CREATED          STATUS          PORTS
                           NAMES
dac871595572   mongo:latest             "docker-entrypoint.s…"    11 minutes ago   Up 11 minutes   0.0.0.0:27017->27017/tcp, :::27017->27017/tcp   stocks_realtime-mongodb-1
ce9d45181c95   python:3.9               "bash -c '\n  apt upd…"   11 minutes ago   Up 11 minutes
                           stocks_realtime-pyparsers-1
6968a93f6181   portainer/agent:2.16.1   "./agent"                 46 minutes ago   Up 46 minutes   0.0.0.0:9001->9001/tcp, :::9001->9001/tcp       portainer_agent
```
6. Tail the pyparser.log file to ensure the program is working correctly.
*I annotated the example with comments (ex: # INSERT EVENT LOG) to identify each event type expected if the program is functioning correctly.*
```
root@twelvedata:/home/mark/stocks_realtime# docker exec ce9d45181c95 tail -f /var/log/pyparser.log
INFO:root:{'event': 'heartbeat', 'status': 'ok'}                                    # HEARTBEAT FROM WEBSOCKET
INFO:root:<pymongo.results.InsertOneResult object at 0x7f1dfa6431f0>                # INSERT EVENT LOG
INFO:root:{'event': 'price', 'symbol': 'GRT/BTC', 'currency_base': 'The Graph', 'currency_quote': 'Bitcoin', 'exchange': 'Huobi', 'type': 'Digital Currency', 'timestamp': 1668886352, 'price': 3.61e-06, 'bid': 3.6e-06, 'ask': 3.62e-06, 'day_volume': 73740, '_id': ObjectId('63792f5075127fbc251c9337')}                                                       # EVENT RECIEVED LOG
INFO:root:<pymongo.results.InsertOneResult object at 0x7f1dfa6432b0>                # INSERT EVENT LOG
INFO:root:{'event': 'price', 'symbol': 'BTC/USD', 'currency_base': 'Bitcoin', 'currency_quote': 'US Dollar', 'exchange': 'Coinbase Pro', 'type': 'Digital Currency', 'timestamp': 1668886352, 'price': 16608.9, 'bid': 16608.9, 'ask': 16608.9, 'day_volume': 10798, '_id': ObjectId('63792f5175127fbc251c9338')}                                           # EVENT RECIEVED LOG
INFO:root:{'event': 'heartbeat', 'status': 'ok'}                                    # HEARTBEAT FROM WEBSOCKET
INFO:root:<pymongo.results.InsertOneResult object at 0x7f1dfa6439a0>                # INSERT EVENT LOG
```
7. You are now ready to access MongoDB using the public ip, port, username, and password you defined in your `.env` file above. 