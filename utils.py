#!interpreter
# -*- coding: utf-8 -*-
import pandas as pd
import ccxt
import json
import time
import smtplib
import ssl
import os
import sys


class ExchangeLog():
    """Log to an exchange from a given JSON config file by using ccxt library

    """

    def __init__(self, exchange_id, conf_path):

        """Extract exchange name, api credential, type of account
        """

        self.exchange_id = exchange_id
        self.conf_path = conf_path
        print("Log to %s ..." %(self.exchange_id))
        if os.path.isfile(self.conf_path):
            
            self.exchange_conf = pd.read_json(conf_path)
            self.api_key = self.exchange_conf['exchange'][self.exchange_id]['api_source_key']
            self.secret_key = self.exchange_conf['exchange'][self.exchange_id]['api_source_secret']
            self.exchange_type = self.exchange_conf['exchange'][self.exchange_id]['type']         
        else:
            print('Could not find the config file to log')

    def log(self):

        """log to the exchange with the credentials from the config file.

        Returns:
            [class]: return an intentiate class of the logged exchange
        """

        exchange_class = getattr(ccxt, self.exchange_id)
        exchange = exchange_class({
            'apiKey': self.api_key,
            'secret': self.secret_key,
            'timeout': 50000,
            'enableRateLimit': True,
            'options': {
                'defaultType': self.exchange_type,
            },
        })
        print("Succesfully logged to %s succesfull" %(self.exchange_id))
        return exchange


def extract_usdt_pair(exchange):

    symbols = list(exchange.fetch_tickers())
    df = pd.DataFrame({'symbol':symbols})
    df = df[df['symbol'].str.contains("/USDT")]
    df = df.reset_index(drop=True)
    return df

def save_json(df,filename):

    df.to_json(filename)


def read_json(filename):

    return pd.read_json(filename)

def detect_new_symbol(listing, new_listing):
    
    df_listing = pd.read_json(listing)
    df_new_listing = pd.read_json(new_listing)
    new_symbol = pd.concat([df_listing,df_new_listing]).drop_duplicates(keep=False)
    new_symbol = new_symbol.reset_index(drop=True)

    return new_symbol


def send_notification(symbol, conf_path):

    if os.path.isfile(conf_path):
        conf = pd.read_json(conf_path)
        email = conf['email']['email_adress']
        password = conf['email']['email_password']

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sent_from = email
    to = [email]
    subject = f'New token on Binance'
    body = f'New token as been listed: ' + symbol
    message = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sent_from, password)
            server.sendmail(sent_from, to, message)

    except Exception as e:
        print(e)


def create_buyorder(exchange, cost, symbol):

    price = exchange.fetch_ticker(symbol=symbol)
    price = price['last']
    amount = cost / price
    log_buyorder = exchange.createOrder(symbol, 'market', 'buy', amount)
    
    return log_buyorder


def create_sellorder(exchange, cost, symbol):

    price = exchange.fetch_ticker(symbol=symbol)
    price = price['last']
    amount = cost / price
    log_sellorder = exchange.createOrder(symbol, 'market', 'sell', amount)

    return log_sellorder