#!interpreter
# -*- coding: utf-8 -*-
import pandas as pd
import ccxt
import json
import time
from exchange_logger import ExchangeLog
from utils import extract_usdt_pair
from utils import detect_new_listing
from utils import send_notification
from utils import create_buyorder
from utils import create_sellorder

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

            new_symbol = new_listing['symbol'].values[0]
            # buy process
            #log_buy = create_buyorder(exchange=binance, cost=100, symbol=new_symbol)
            time.sleep(10)
            #log_sell = create_sellorder(exchange=binance, cost=100, symbol=new_symbol)
            # re initialization for a new token listing 
            listing = new_listing
            send_notification(symbol=new_symbol, conf_path='.config.json')

        time.sleep(0.05)