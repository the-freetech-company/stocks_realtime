import json
import logging
import os
from pymongo import MongoClient
import sched
import time
import uuid
from twelvedata import TDClient

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
    sc.enter(60, 1, pull_ohlc_one, (sc, tickers))
    for x in tickers:
        # pull td data and convert to df
        one_min = td.time_series(
            symbol=x,
            interval="1min",
            outputsize=6,
            timezone="America/New_York",
        )
        one_df = one_min.as_pandas().reset_index()

        # add labels, calc diff
        one_df["ticker"] = x
        one_df["delta"] = one_df["close"].diff()

        # drop initial row used for calculation
        one = one_df.iloc[1:, :]

        # insert into mongo
        logging.info(collection_ohlc_one_min.insert_many(json.loads(one.to_json(orient="records"))))
    logging.info(f"OHLC 1 Min #{uid} finished.")


def pull_ohlc_five(sc, tickers):
    uid = str(uuid.uuid4())
    logging.info("OHLC 5 Min #{uid} started.")
    # schedule next execution
    sc.enter(300, 1, pull_ohlc_five, (sc, tickers))
    for x in tickers:
        # pull td data and convert to df
        five_min = td.time_series(
            symbol=x,
            interval="5min",
            outputsize=2,
            timezone="America/New_York",
        )
        five_df = five_min.as_pandas().reset_index()

        # add labels, calc diff
        five_df["ticker"] = x
        five_df["delta"] = five_df["close"].diff()

        # drop initial row used for calculation
        five = five_df.iloc[1:, :]

        # insert into mongo
        collection_ohlc_five_min.insert_many(json.loads(five.to_json(orient="records")))
    logging.info(f"OHLC 5 Min #{uid} finished.")


s.enter(0, 1, pull_ohlc_one, (s, os.environ["SYMBOLS"]))
s.enter(0, 1, pull_ohlc_five, (s, os.environ["SYMBOLS"]))
s.run()
