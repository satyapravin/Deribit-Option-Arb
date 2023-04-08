import json
from PyQt6 import QtCore, QtWebSockets, QtNetwork


# create a websocket object
class Deribit_WS(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.ids = { "default": 1,
                     "authenticate": 2, 
                     "accounts": 3,
                     "changes": 4,
                     "tickers": 5,
                    }
        self.authenticated = False
        self.controller = None

    
    def connect(self, controller, client_id, client_secret, client_url):
        self.controller = controller
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_url = client_url
        self.json = {
            "jsonrpc" : "2.0",
            "id" : 1,
            "method" : None,
        }

        self.client =  QtWebSockets.QWebSocket("Deribit_Socket",QtWebSockets.QWebSocketProtocol.Version.VersionLatest, None)
        self.client.error.connect(self.error)
        self.client.textMessageReceived.connect(self.onMessage)
        
        self.client.open(QtCore.QUrl(self.client_url))

    def authenticate(self):
        options = {
            "grant_type" : "client_credentials",
            "client_id" : self.client_id,
            "client_secret" : self.client_secret
        }

        self.json["method"] = "public/auth"
        self.json["id"] = self.ids["authenticate"]
        self.json["params"] = options
        auth = json.dumps(self.json)
        self.client.sendTextMessage(auth)

    def onMessage(self, textMessage):
        response = json.loads(textMessage)
        if "id" in response and response["id"] == 2:
            if "result" in response:
                if "token_type" in response['result']:
                    print("Authenticated")
                    self.authenticated = True
        else:
            if "params" in response and "channel" in response["params"]:
                channel = response["params"]["channel"]
                if channel.startswith("user.portfolio."):
                    if "data" in response['params']:
                        self.controller.onAccountData(response["params"]["data"])
                if channel.startswith("user.changes."):
                    if 'data' in response:
                        data = response['data']
                        if 'positions' in data:
                            self.controller.onPositionData(response["data"]["positions"])
                if channel.startswith("ticker."):
                    self.controller.onMarketData(response["params"]["data"])

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())

    # send an authentication request
    def call_api(self, request):
        return self.client.sendTextMessage(json.dumps(request))

    def limit_buy_aggressive(self, instrument_name, amount, reduce_only, price):
        self.buy_raw(instrument_name, amount, "limit", reduce_only, price, False)
    
    def buy_market(self, instrument_name, amount, reduce_only):
        self.buy_raw(instrument_name, amount, "market", reduce_only, None, False)

    def limit_buy_passive(self, instrument_name, amount, reduce_only, price):
        self.buy_raw(instrument_name, amount, "limit", reduce_only, price, True)

    def buy_raw(self, instrument_name, amount, order_type, reduce_only, price, post_only):
        options = {
            "instrument_name" : instrument_name,
            "amount" : amount,
            "type" : order_type,
            "reduce_only" : reduce_only,
        }

        if price:
            options["price"] = price
        if post_only:
            options["post_only"] = post_only

        self.json["method"] = "private/buy"
        self.json["id"] = self.ids["default"]
        self.json["params"] = options
        return self.call_api(self.json)
    
    def limit_sell_aggressive(self, instrument_name, amount, reduce_only, price):
        self.sell_raw(instrument_name, amount, "limit", reduce_only, price, False)
    
    def sell_market(self, instrument_name, amount, reduce_only):
        self.sell_raw(instrument_name, amount, "market", reduce_only, None, False)

    def limit_sell_passive(self, instrument_name, amount, reduce_only, price):
        self.sell_raw(instrument_name, amount, "limit", reduce_only, price, True)

    def sell_raw(self, instrument_name, amount, order_type, reduce_only, price, post_only):
        options = {
            "instrument_name" : instrument_name,
            "amount" : amount,
            "type" : order_type,
            "reduce_only" : reduce_only,
        }

        if price:
            options["price"] = price
        if post_only:
            options["post_only"] = post_only

        self.json["method"] = "private/sell"
        self.json["id"] = self.ids["default"]
        self.json["params"] = options

        return self.call_api(self.json)

    def edit(self, order_id, amount, price):
        options= {
            "order_id" : order_id,
            "amount" : amount,
            "price" : price
        }

        self.json["method"] = "private/edit"
        self.json["id"] = self.ids["default"]
        self.json["params"] = options
        return self.call_api(self.json)

    def cancel(self, order_id):
        options = {"order_id" : order_id}
        self.json["method"] = "private/cancel"
        self.json["id"] = self.ids["default"]
        self.json["params"] = options
        return self.call_api(self.json)

    def cancel_all(self):
        self.json["method"] = "private/cancel_all"
        self.json["id"] = self.ids["default"]
        return self.call_api(self.json)

    def change_summary(self, currency):
        options = {"channels" : ["user.changes.option." + currency + ".100ms"]}
        self.json["method"] = "private/subscribe"
        self.json["id"] = self.ids["changes"]
        self.json["params"] = options
        return self.call_api(self.json)
    
    def account_summary(self, currency):
        options = {"channels" : ["user.portfolio." + currency]}
        self.json["method"] = "private/subscribe"
        self.json["id"] = self.ids["accounts"]
        self.json["params"] = options
        return self.call_api(self.json)

    def ticker(self, instrument_name):
        options = {"channels" : ["ticker." + instrument_name + ".100ms"]}
        self.json["method"] = "public/subscribe"
        self.json["id"] = self.ids["tickers"]
        self.json["params"] = options
        return self.call_api(self.json)

    def unsubscribe_all_public(self):
        self.json["method"] = "public/unsubscribe_all"
        options = {}
        self.json["id"] = self.ids["default"]
        self.json["params"] = options
        return self.call_api(self.json)
    
    def unsubscribe_all_private(self):
        self.json["method"] = "private/unsubscribe_all"
        options = {}
        self.json["id"] = self.ids["default"]
        self.json["params"] = options
        return self.call_api(self.json)
    
    def close(self):
        self.unsubscribe_all_private()
        self.unsubscribe_all_public()
        print("Closing websocket")
        self.client.close()