import ccxt
import configparser
import json

if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read("config\\config.ini")
    key = "TEST"
    api_key = cfg[key]["api_key"]
    api_secret = cfg[key]["api_secret"]
    exch = ccxt.deribit({'apiKey': api_key, 'secret': api_secret})
    exch.set_sandbox_mode(True)
    exch.quoteJsonNumbers = False
    response = exch.fetch2("get_portfolio_margins", "private", params={"currency": "BTC"})
    print(response)