#types of tokens for parsing

class Abstraction():
	def __init__(self, param, body):
		self.param = param
		self.body = body

	def toString(self):
		return ('ABS (λ' + self.param + '.' + self.body.toString() + ')')

class Application():
	def __init__(self, lhs, rhs):
		self.rhs = rhs #right hand side of equation
		self.lhs = lhs #left hand side

	def toString(self):
		return ("APP " + self.lhs.toString() + self.rhs.toString())

class Identifier(): #aka variable
	def __init__(self, value, name):
		self.value = value
		self.name = name

	def toString(self):
		return ("ID " + self.name)
