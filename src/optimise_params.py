class OptimiseParams:
    def __init__(self):
        self.minimize = True
        self.currObjective = "Min Cost"
        self.maxDeltaPct = 0.01
        self.minTheta = 5
        self.minGammaBps = 0.001
        self.putNeutral = True
        self.callNeutral = True
        self.positiveVega = True
        self.longPut = True
        self.longCall = True
        self.maxUnit = 5
        self.maxTotal = 15
        self.usePositions = True
        self.maxSpreadBps = 0.001
        self.contract_size = 1
        self.doubleFee = True

    @staticmethod
    def create_default():
        return OptimiseParams()