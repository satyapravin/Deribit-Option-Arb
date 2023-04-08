
class Results:
	def __init__(self):
		self.delta = 0
		self.gamma = 0
		self.vega = 0
		self.theta = 0
		self.net_income = 0
		self.income = 0
		self.fees = 0
		self.margin = 0		
		self.expiryMargin = 0
		self.cols = 9
	
	def clear(self):
		self.delta = 0
		self.gamma = 0
		self.vega = 0
		self.theta = 0
		self.net_income = 0
		self.income = 0
		self.fees = 0
		self.margin = 0		
		self.expiryMargin = 0
		self.cols = 9

	def getRows(self):
		return 2
		
	def getCols(self):
		return self.cols
		
	def getData(self, j, i):
		if j == 0:
			if i == 0:
				return "Delta"
			elif i == 1:
				return "Gamma"
			elif i == 2:
				return "Vega"
			elif i == 3:
				return "Theta"
			elif i == 4:
				return "NetIncome"
			elif i == 5:
				return "Income"
			elif i == 6:
				return "Fees"
			elif i == 7:
				return "Margin"
			elif i == 8:
				return "Next Margin"
			else:
				return ""
		else:
			if i == 0:
				return self.delta
			elif i == 1:
				return self.gamma
			elif i == 2:
				return self.vega
			elif i == 3:
				return self.theta
			elif i == 4:
				return self.net_income
			elif i == 5:
				return self.income
			elif i == 6:
				return self.fees
			elif i == 7:
				return self.margin
			elif i == 8:
				return self.expiryMargin
			else:
				return 0