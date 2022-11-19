from websocket import create_connection, WebSocketConnectionClosedException
import json
from pymongo import MongoClient
import logging
import os
import time
from twelvedata import TDClient
# for dev
# from dotenv import load_dotenv
# load_dotenv()


logging.basicConfig(filename='pyparser.log', level=logging.INFO)

mg = MongoClient("192.168.1.38", 27017,
                 username="mongo",
                 password="mongo")
collection = mg['stockdb']['prices']
logging.info(collection)

messages_history = []

def on_event(e):
    if len(messages_history) > 0:
        collection.insert_many(messages_history)
    logging.info(str(e))





td = TDClient(apikey=os.environ["API_KEY"])
ws = td.websocket(symbols=["0xBTC/BTC", "ETH/BTC", "BTC/USD", "GRT/BTC", "XRP/BTC", "DOGE/BTC", "BNB/BTC"], on_event=on_event)
# ws.subscribe()
ws.connect()
while True:
    logging.info('messages received: ', len(messages_history))
    ws.heartbeat()
    time.sleep(5)