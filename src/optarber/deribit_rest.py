import datetime
import json as json
import ccxt 

class RestClient(object):
    def __init__(self, key, secret, Test=True):
        self.key = key
        self.secret = secret
        self.session = ccxt.deribit({'apiKey': key, 'secret': secret})
        self.session.set_sandbox_mode(Test)
        self.session.quoteJsonNumbers = False

    def call_api(self, command, access, options):
        response = self.session.fetch2(command, access, params=options)
        return response

    def getinstruments(self, currency, kind):
        '''
        to get available trading instruments
        input:
            currency: string ['BTC', 'ETH']
            kind:string [eg: 'future' or 'option']
        '''
        assert kind in ['future','option']
        
        options = {
            'currency': currency,
            'kind':kind
        }

        response = self.call_api("get_instruments", "public", options)

        if "result" in response:
            return response["result"]
        else:
            return {}
    
    
    def getportfoliomargin(self, curr, instrs):
        
        options = {
             'currency':curr, 
             'simulated_positions': json.dumps(instrs),
             'add_positions': 'true'
        }

        response = self.call_api("get_portfolio_margins", "private", options)

        if "result" in response:
            return response['result']
        else:
            return {}
    

    def getinstrument(self, instr):
        options = {
            'instrument_name': instr,
        }

        response = self.call_api("get_instrument", "public", options)
        if "result" in response:
            return response["result"]
        else:
            return {}
    
    

    def getindex(self, currency):
        options = {
            "currency":currency,
            }

        response = self.call_api("get_index", "public", options)
        if "result" in response:
            return response["result"]
        else:
            return {}
    
    def getopenorders(self, currency, kind):
        '''
        to retrieve pending orders [order not yet settled]
        input:
            currency: string in 'BTC' or 'ETH'
        output:
            [ID1, ID2...]
        '''
        options = {
            "currency":currency,
            "kind": kind
            }

        return self.call_api("get_open_orders_by_currency", "private", options);


    def getpositions(self, currency, kind):
        '''
        to retrieve position by currency
        input:
            currency: string in 'BTC' or 'ETH'
        return: 
            int [size of position. positive for 'buy' and negative for 'sell'
            
        '''

        options = {
            "currency":currency,
            "kind": kind
            }
        response = self.call_api("get_positions", "private", options);

        if "result" in response:
            return response["result"]
        else:
            return []
    

    def buy(self, instrument, quantity, price, postOnly=None, time_in_force="fill_or_kill"):
        options = {
            "instrument_name": instrument,
            "amount": quantity,
            "price": price,
            "time_in_force": time_in_force
        }
  
        if postOnly:
            options["postOnly"] = postOnly

        return self.call_api("buy", "private", options)


    def sell(self, instrument, quantity, price, postOnly=None, time_in_force="fill_or_kill"):
        options = {
            "instrument_name": instrument,
            "amount": quantity,
            "price": price,
            "time_in_force": time_in_force
        }

        if postOnly:
            options["postOnly"] = postOnly

        return self.call_api("sell", "private", options)
