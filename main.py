#!interpreter
# -*- coding: utf-8 -*-
import pandas as pd
import ccxt
import json
import time
from utils import ExchangeLog
from utils import extract_usdt_pair
from utils import send_notification
from utils import create_buyorder
from utils import create_sellorder
from utils import save_json
from utils import detect_new_symbol
import os

if __name__ == "__main__":
    
    exchange = ExchangeLog(exchange_id='binance',conf_path='.config.json')
    exchange = exchange.log()
    filename_listing = 'listing.json'
    filename_new_listing = 'new_listing.json'

    # initialization
    listing = extract_usdt_pair(exchange=exchange)
    save_json(listing,filename_listing)

    while True:
        
        try:
            new_listing = extract_usdt_pair(exchange=exchange)
            save_json(new_listing,filename_new_listing)

        except Exception as err:
            print(err)
            continue

        new_symbol = detect_new_symbol(filename_listing, filename_new_listing)
        if not new_symbol.empty:

            print('New symbol detected')
            print(new_symbol['symbol'][0])
            symbol = new_symbol['symbol'][0]
            # buy process
            #log_buy = create_buyorder(exchange=binance, cost=100, symbol=new_symbol)
            #log_sell = create_sellorder(exchange=binance, cost=100, symbol=new_symbol)
            # re initialization for a new token listing
            save_json(new_listing,filename_listing)
            send_notification(symbol=symbol, conf_path='.config.json')
        
        time.sleep(1)