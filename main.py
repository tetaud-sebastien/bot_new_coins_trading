#!interpreter
# -*- coding: utf-8 -*-
import pandas as pd
import ccxt
import json
from exchange_logger import ExchangeLog


# log 
binance = ExchangeLog(exchang_id='binance',conf_path='.config.json')
binance = binance.log()

def extract_usdt_pair(exchange):

    symbols = list(exchange.fetch_tickers())
    df = pd.DataFrame({'symbol':symbols})
    df = df[df['symbol'].str.contains("/USDT")]
    return df

def detect_new_listing(exchange, listing):

    symbols = list(exchange.fetch_tickers())
    df = pd.DataFrame({'symbol':symbols})
    df = df[df['symbol'].str.contains("/USDT")]
    new_listing = pd.concat([df,listing]).drop_duplicates(keep=False)
    return new_listing



listing = extract_usdt_pair(exchange=binance)
new_listing = detect_new_listing(binance, listing)

if len(new_listing) > 0:
    print(new_listing)