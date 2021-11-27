import pandas as pd
import ccxt
import json
import time
from exchange_logger import ExchangeLog

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