
class SelectionData:
	def __init__(self):
		self.positions = []
		self.cols = 10
	
	def clear(self):
		self.positions = []
		self.cols = 10

	def update(self, positions):
		self.positions = positions
		
	def getRows(self):
		return len(self.positions) + 1
		
	def getCols(self):
		return self.cols
		
	def getData(self, j, i):
		if j == 0:
			if i == 0:
				return "Instr"
			elif i == 1:
				return "Size"
			elif i == 2:
				return "BidAmount"
			elif i == 3:
				return "BidPrice"
			elif i == 4:
				return "AskPrice"
			elif i == 5:
				return "AskAmount"
			elif i == 6:
				return "Delta"
			elif i == 7:
				return "Gamma"
			elif i == 8:
				return "Vega"
			elif i == 9:
				return "Theta"
			else:
				return ""
		else:
			op = self.positions[j-1].op
			size = self.positions[j-1].size
			
			if i == 0:
				return op.name
			elif i == 1:
				return size
			elif i == 2:
				return op.bid_amount
			elif i == 3:
				return op.bid_price
			elif i == 4:
				return op.ask_price
			elif i == 5:
				return op.ask_amount
			elif i == 6:
				return size * op.delta
			elif i == 7:
				return size * op.gamma
			elif i == 8:
				return size * op.vega
			elif i == 9:
				return size * op.theta
			else:
				return 0