import json
import logging
import os
from pymongo import MongoClient
import sched
import time
import uuid
from twelvedata import TDClient
from datetime import datetime

logging.basicConfig(filename='/var/log/pyparser.log', level=logging.INFO)

mg = MongoClient(os.environ['MONGO_PUBLIC_IP'], int(os.environ['MONGO_PORT']),
                 username=os.environ['MONGO_USER'],
                 password=os.environ['MONGO_PASSWORD'])
collection_ohlc_one_min = mg['stockdb']['ohlc_one_min']
collection_ohlc_five_min = mg['stockdb']['ohlc_five_min']
logging.info(collection_ohlc_one_min)
logging.info(collection_ohlc_five_min)

td = TDClient(apikey=os.environ["API_KEY"])
s = sched.scheduler(time.time, time.sleep)


def pull_ohlc_one(sc, tickers):
    uid = str(uuid.uuid4())
    logging.info("OHLC 1 Min #{uid} started.")
    # schedule next execution
    for x in tickers:
        # pull td data and convert to df
        one_min = td.quote(
            symbol=x,
            interval="1min",
            prepost=True,
            timezone="America/New_York",
        )
        one_df = one_min.as_pandas().reset_index()

        # add labels, calc diff
        one_df["ticker"] = x
        one_df["delta"] = one_df["close"].diff()

        # drop initial row used for calculation
        one = one_df.iloc[1:, :]

        # insert into mongo
        one = json.loads(one.to_json(orient="records", date_format='iso'))
        for i, obj in enumerate(one):
            one[i]['datetime'] = datetime.strptime(one[i]['datetime'], "%Y-%m-%dT%H:%M:%S.%f")
        logging.info(collection_ohlc_one_min.insert_many(one))
    logging.info(f"OHLC 1 Min #{uid} finished.")
    sc.enter(60, 1, pull_ohlc_one, (sc, tickers))


def pull_ohlc_five(sc, tickers):
    uid = str(uuid.uuid4())
    logging.info("OHLC 5 Min #{uid} started.")
    # schedule next execution
    for x in tickers:
        # pull td data and convert to df
        five_min = td.quote(
            symbol=x,
            interval="5min",
            prepost=True,
            timezone="America/New_York",
        )
        five_df = five_min.as_pandas().reset_index()

        # add labels, calc diff
        five_df["ticker"] = x
        five_df["delta"] = five_df["close"].diff()

        # drop initial row used for calculation
        five = five_df.iloc[1:, :]

        # insert into mongo
        five = json.loads(five.to_json(orient="records", date_format='iso'))
        for i, obj in enumerate(five):
            five[i]['datetime'] = datetime.strptime(five[i]['datetime'], "%Y-%m-%dT%H:%M:%S.%f")
        logging.info(collection_ohlc_one_min.insert_many(five))
    logging.info(f"OHLC 5 Min #{uid} finished.")
    sc.enter(300, 1, pull_ohlc_five, (sc, tickers))


s.enter(0, 1, pull_ohlc_one, (s, json.loads(os.environ["SYMBOLS"])))
# s.enter(0, 1, pull_ohlc_five, (s, json.loads(os.environ["SYMBOLS"])))
s.run()
