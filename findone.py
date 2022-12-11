import json
import logging
import os
from pymongo import MongoClient
import sched
import time
import uuid
from twelvedata import TDClient
from dotenv import load_dotenv, find_dotenv
from typing import TypedDict
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# logging.basicConfig(filename='/var/log/pyparser.log', level=logging.INFO)

mg = MongoClient(os.environ['MONGO_PUBLIC_IP'], int(os.environ['MONGO_PORT']),
                 username=os.environ['MONGO_USER'],
                 password=os.environ['MONGO_PASSWORD'])
collection_ohlc_one_min = mg['stockdb']['ohlc_one_min']
collection_ohlc_five_min = mg['stockdb']['ohlc_five_min']

print(collection_ohlc_one_min.find_one())
