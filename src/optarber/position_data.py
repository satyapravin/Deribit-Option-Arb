
class PositionData:
	def __init__(self):
		self.keys = {}
		self.positions = []
		self.cols = 6
	
	def clear(self):
		self.positions = []
		self.cols = 6

	def add(self, positions):
		self.keys = {}
		self.positions = []

		for i, pos in enumerate(positions):
			name = pos.op.name
			self.keys[name] = i
			self.positions.append(pos)

	def update(self, positions):
		for pos in positions:
			name = pos['instrument_name']
			if name in self.keys:
				pos = self.positions[self.keys[name]]
				pos.size = pos['size']
				opt = pos.op
				opt.delta = pos['delta'] / opt.size
				opt.gamma = pos['gamma'] / opt.size
				opt.vega = pos['vega'] / opt.size
				opt.theta = pos['theta'] / opt.size
		
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
				return "Delta"
			elif i == 3:
				return "Gamma"
			elif i == 4:
				return "Vega"
			elif i == 5:
				return "Theta"
			else:
				return ""
		else:
			pos = self.positions[j-1]
			
			if i == 0:
				return pos.op.name
			elif i == 1:
				return pos.size
			elif i == 2:
				return pos.op.delta * pos.size
			elif i == 3:
				return pos.op.gamma * pos.size
			elif i == 4:
				return pos.op.vega * pos.size
			elif i == 5:
				return pos.op.theta * pos.size
			else:
				return 0