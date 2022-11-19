from websocket import create_connection, WebSocketConnectionClosedException
import json
from pymongo import MongoClient
import logging
import os
import time
from twelvedata import TDClient
# for dev
from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(filename='pyparser.log', level=logging.INFO)

mg = MongoClient("192.168.1.38", 27017,
                 username="mongo",
                 password="mongo")
collection = mg['stockdb']['prices']
logging.info(collection)

def on_event(e):
    if len(messages_history) > 0:
        collection.insert_many(messages_history)
    print(e)

messages_history = []

td = TDClient(apikey=os.environ["API_KEY"])
ws = td.websocket(symbols=["BTC/USD","ETH/USD", "CRO/USD"], on_event=on_event)
ws.subscribe(["BTC/USD", "ETH/USD", "CRO/USD"])
ws.connect()
while True:
    print('messages received: ', len(messages_history))
    ws.heartbeat()
    time.sleep(5)