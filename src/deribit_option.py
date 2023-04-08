class Option:
    def __init__(self, name, kind, expiry, strike, delta, gamma, vega, theta, 
			       bid_price, bid_amount, ask_price, ask_amount):
        self.name = name
        self.kind = kind
        self.expiry = expiry
        self.strike = strike
        self.delta = delta
        self.gamma = gamma
        self.vega = vega
        self.theta = theta
        self.bid_price = bid_price
        self.bid_amount = bid_amount
        self.ask_price = ask_price
        self.ask_amount = ask_amount