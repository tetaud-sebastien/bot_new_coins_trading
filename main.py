#!interpreter
# -*- coding: utf-8 -*-
import pandas as pd
import ccxt
import json
import time
from exchange_logger import ExchangeLog
from utils import extract_usdt_pair
from utils import detect_new_listing


if __name__ == "__main__":
    
    binance = ExchangeLog(exchang_id='binance',conf_path='.config.json')
    binance = binance.log()
    # initialization
    listing = extract_usdt_pair(exchange=binance)

    while True:
        
        try:
            new_listing = detect_new_listing(binance, listing)
        except Exception as err:
            print(err)
            continue

        if len(new_listing) > 0:

            new_pair = new_listing['symbol'].values[0]
            
            # buy process
            # re initialization for a new token listing 
            listing = new_listing
        else:
            print('no token found')
        time.sleep(1)