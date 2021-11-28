import pandas as pd
import ccxt
import json
import time
import smtplib
import ssl
import os
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