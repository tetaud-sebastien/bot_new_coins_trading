#!interpreter
# -*- coding: utf-8 -*-
"""main script
"""
import os
import sys
import ccxt
import pandas as pd


class ExchangeLog():
    """Log to an exchange from a given JSON config file by using ccxt library

    """

    def __init__(self, exchang_id, conf_path):

        """Extract exchange name, api credential, type of account
        """

        self.exchang_id = exchang_id
        self.conf_path = conf_path
        print("Log to %s ..." %(self.exchang_id))
        if os.path.isfile(self.conf_path):
            
            self.exchange_conf = pd.read_json(conf_path)
            self.api_key = self.exchange_conf['exchange'][self.exchang_id]['api_source_key']
            self.secret_key = self.exchange_conf['exchange'][self.exchang_id]['api_source_secret']
            self.exchange_type = self.exchange_conf['exchange'][self.exchang_id]['type']         
        else:
            print('Could not find the config file to log')

    def log(self):

        """log to the exchange with the credentials from the config file.

        Returns:
            [class]: return an intentiate class of the logged exchange
        """

        exchange_class = getattr(ccxt, self.exchang_id)
        exchange = exchange_class({
            'apiKey': self.api_key,
            'secret': self.secret_key,
            'timeout': 50000,
            'enableRateLimit': True,
            'options': {
                'defaultType': self.exchange_type,
            },
        })
        print("Succesfully logged to %s succesfull" %(self.exchang_id))
        return exchange
