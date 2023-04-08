import asyncio
import ccxt
import configparser
import logging
import requests
import time

class Scalper:
    def __init__(self, config_file, exchange):
        try:
            cfg = configparser.ConfigParser()
            cfg.read(config_file)
            self._api_key = cfg[exchange]['api_key']
            self._api_secret = cfg[exchange]['api_secret']
            self.symbol = cfg[exchange]['symbol']
            self.price_move = round(float(cfg[exchange]['price_move']), 2)
            self.hedge_lookup = cfg[exchange]['hedge_lookup']
            self.hedge_contract = cfg[exchange]['hedge_contract']
            self.ladder_size = int(cfg[exchange]['ladder_size'])
            self.tick_size = round(float(cfg[exchange]['tick_size']), 2)
            self.delta_threshold = float(cfg[exchange]['delta_threshold'])
            self.done = False
            if exchange == "Deribit":
                self.exchange = ccxt.deribit({'apiKey': self._api_key, 'secret': self._api_secret})
                self.exchange.set_sandbox_mode(True)
            else:
                raise Exception("Exchange " + exchange + " not yet supported")

            if self.symbol != "BTC" and self.symbol != "ETH":
                raise Exception("Only BTC and ETH supported symbols")

        except  Exception as e:
            logging.error("Failed to initialize configuration from file " + config_file, e)
    
    async def get_option_greeks(self):
        delta = float(self.exchange.fetch_balance({'currency': str(self.symbol)})['info']['options_delta'])
        gamma = float(self.exchange.fetch_balance({'currency': str(self.symbol)})['info']['options_gamma'])
        return delta, gamma

    async def get_hedge_delta(self):
        lookup = self.exchange.fetch_balance({'currency': str(self.symbol)})
        hedge_lookup = lookup['info']['delta_total_map']

        if self.hedge_lookup in hedge_lookup:
            return float(hedge_lookup[self.hedge_lookup])
        else:
            return 0

    async def get_open_orders(self, symbol):
        return self.exchange.fetch_open_orders(symbol)

    async def get_ticker(self, symbol):
        ticker = self.exchange.publicGetTicker({"instrument_name": symbol})
        ticker = ticker['result']
        return float(ticker["best_bid_price"]), float(ticker["best_ask_price"]), float(ticker['mark_price'])

    async def get_order_book(self, symbol):
        orderbook = self.exchange.fetch_l2_order_book(symbol, 40)
        bids = orderbook['bids']
        asks = orderbook['asks']
        return bids, asks


    async def get_new_delta(self, net_delta, option_gamma, move):
        return net_delta + option_gamma * move 

    async def delta_hedge(self, prev_index, prev_delta):
        # get greeks
        option_delta, option_gamma = await self.get_option_greeks()
        hedge_delta = await self.get_hedge_delta()
        net_delta = option_delta + hedge_delta

        proposed_bids = {}
        proposed_asks = {}
        best_bid_price, best_ask_price, mark_price = await self.get_ticker(self.hedge_contract)
        index_price = (best_ask_price + best_bid_price) * 0.5

        if index_price == prev_index and abs(net_delta - prev_delta) > self.delta_threshold:
            return index_price, prev_delta
    
        if abs(net_delta) < self.delta_threshold:
            print("not need to hedge")
            return index_price, net_delta

        self.exchange.cancel_all_orders(self.hedge_contract)

        print("bid price", best_bid_price, "ask price", best_ask_price, "mark price", mark_price)
        print("delta", round(net_delta, 4), "option delta", round(option_delta, 4), "hedge delta", round(hedge_delta, 4))
        
        net_bid_delta = 0
        net_ask_delta = 0        
        
        for ladder in range(self.ladder_size):
            bid_price_delta = self.price_move * ladder
            ask_price_delta = bid_price_delta

            new_bid_price = round(round((best_bid_price - bid_price_delta) / self.tick_size) * self.tick_size, 2)
            bdelta = await self.get_new_delta(net_delta, option_gamma, new_bid_price - best_bid_price) - net_bid_delta
            
            if bdelta * new_bid_price < -50:
                print("bid ladder", ladder, new_bid_price, abs(bdelta) * new_bid_price)
                proposed_bids[new_bid_price] = round(abs(bdelta) * new_bid_price, 0)
                net_bid_delta += bdelta

            new_ask_price = round(round((best_ask_price + ask_price_delta) / self.tick_size) * self.tick_size, 2)
            adelta = await self.get_new_delta(net_delta, option_gamma, new_ask_price - best_ask_price) - net_ask_delta
            
            if adelta * new_ask_price > 50:
                print("ask ladder", ladder, new_ask_price, adelta * new_ask_price)
                proposed_asks[new_ask_price] = round(adelta * new_ask_price, 0)
                net_ask_delta += adelta

        # submit orders
        for bid_price in proposed_bids:
            print("bid_ladder", bid_price, proposed_bids[bid_price])
            self.exchange.create_limit_buy_order(self.hedge_contract, proposed_bids[bid_price], bid_price, {"post_only": True})

        for ask_price in proposed_asks:
            print("ask_ladder", ask_price, proposed_asks[ask_price])
            self.exchange.create_limit_sell_order(self.hedge_contract, proposed_asks[ask_price], ask_price, {"post_only": True})
        
        print("====================================")
        return index_price, net_delta

    async def get_balance(self, symbol):
        return self.exchange.fetch_balance({'currency': self.symbol})

    async def run_loop(self):
        retry_count = 0
        post_interval = 0
        index_price = 0
        prev_delta = 1
        while not self.done:
            try:
                index_price, prev_delta = await self.delta_hedge(index_price, prev_delta)
                time.sleep(3)
                post_interval += 3

                if post_interval > 300:
                    await self.send_to_telegram()
                    post_interval = 0
                retry_count = 0
            except Exception as e:
                print("Hedge failed", e)
                retry_count += 1
                if retry_count >= 9:
                    self.done = True

    async def send_to_telegram(self):
        apiToken = '5715880531:AAEX0uW87-SHHTGtG6Wh0wJ3z140nm0l5hU'
        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
        chatID = '1182531369'

        try:
            message = self.exchange.fetch_balance({'currency': str(self.symbol)})['info']
            requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        except Exception as e:
            print("telegram error", e)

    def run(self):
        self.done = False
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_loop())
