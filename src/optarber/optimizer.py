import cvxpy as cvx
import numpy as np
from deribit_option_position import DeribitPosition

class Optimizer:
    def __init__(self, params, fetches, positions):
        self.params = params
        self.fetches = fetches
        self.positions = positions

    def compute(self):
        option_dict = {}
        for op in self.fetches:
            if op.ask_price is not None and op.bid_price is not None:
                if (op.ask_price - op.bid_price) <= self.params.maxSpreadBps:
                    option_dict[op.name] = op

        for pos in self.positions:
            if pos.op.name not in option_dict:
                if self.params.usePositions:
                    option_dict[pos.op.name] = pos.op
            else:
                if not self.params.usePositions:
                    option_dict.pop(pos.op.name)

        option_data = list(option_dict.values())

        N = len(option_data)
        deltas = np.zeros(N)
        gammas = np.zeros(N)
        vegas = np.zeros(N)
        thetas = np.zeros(N)
        bids = np.zeros(N)
        bidamounts = np.zeros(N)
        askamounts = np.zeros(N)
        asks = np.zeros(N)
        calls = np.zeros(N)
        puts = np.zeros(N)
        strikes = np.zeros(N)

        for i in range(0, N):
            deltas[i] = option_data[i].delta
            gammas[i] = option_data[i].gamma
            vegas[i] = option_data[i].vega
            thetas[i] = option_data[i].theta
            bids[i] = option_data[i].bid_price
            asks[i] = option_data[i].ask_price
            bidamounts[i] = option_data[i].bid_amount / self.params.contract_size
            askamounts[i] = option_data[i].ask_amount / self.params.contract_size
            kind = 1 if option_data[i].kind[0] == 'c' else -1
            calls[i] = max(kind, 0)
            puts[i] = min(kind, 0)
            strikes[i] = option_data[i].strike
        
        res = self._calculate(list(option_dict.keys()), deltas, gammas, vegas, thetas, bids, asks, bidamounts, askamounts, calls, puts, strikes)

        selections = []

        if res is not None:
            for i, op in enumerate(option_data):
                if res[0, i] != 0:
                    p = DeribitPosition(op, res[0, i])
                    selections.append(p)

        return selections

    def _calculate(self, option_names, deltas, gammas, vegas, thetas, bids, asks, bidamounts, askamounts, calls, puts, strikes):
        N = len(option_names)

        if N == 0:
            return None
        
        x = cvx.Variable((1, N), integer=True)
        y = cvx.Variable((1, N), integer=True)
        p = cvx.Variable((1, N), integer=True)

        obj = None

        if self.params.currObjective == "Min Cost":
            obj = cvx.Minimize(x@asks + y@bids)
        elif self.params.currObjective == "Max Gamma":
            obj = cvx.Maximize((x+y+p)@gammas)
        elif self.params.currObjective == "Max Theta":
            obj = cvx.Maximize((x+y+p)@thetas)
        else:
            return None
        
        cons = [(x+y+p)@deltas <= self.params.maxDeltaPct, 
                (x+y+p)@deltas >= -self.params.maxDeltaPct]
        cons.append((x+y+p)@gammas >= self.params.minGammaBps)
        cons.append((x+y+p)@thetas >= self.params.minTheta)
        if self.params.positiveVega: cons.append((x+y+p)@vegas >= 0)
        if self.params.callNeutral: cons.append((x+y+p)@calls == 0)
        if self.params.putNeutral: cons.append((x+y+p)@puts == 0)
        if self.params.longPut: cons.append(cvx.multiply(y[0, :] + x[0, :] + p[0, :], puts)@strikes <= 0)
        if self.params.longCall: cons.append(cvx.multiply(y[0, :] + x[0, :] + p[0, :], calls)@strikes >= 0)
        cons.append(x <= self.params.maxUnit)
        cons.append(x >= 0)
        cons.append(y >= -self.params.maxUnit)
        cons.append(y <= 0)
        cons.append(cvx.sum(x + cvx.pos(p)) <= self.params.maxTotal)
        cons.append(cvx.sum(y - cvx.neg(p)) >= -self.params.maxTotal)
        
        sizes = np.zeros((1, N))
        if self.params.usePositions:
            for pos in self.positions:
                idx = option_names.index(pos.op.name)
                sizes[0, idx] = pos.size  / self.params.contract_size
        cons.append(p == np.asarray(sizes))

        for i in range(N):
            cons.append(x[0, i] <= askamounts[i])
            cons.append(y[0, i] >= -bidamounts[i])

        prob = cvx.Problem(objective=obj, constraints=cons)
        prob.solve(verbose=1)
        
        if prob.status == 'optimal':
            return np.around((x.value + y.value) * self.params.contract_size, 1)
        else:
            return None