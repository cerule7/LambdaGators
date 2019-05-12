#types of tokens for parsing

class Abstraction():
	def __init__(self, param, body):
		self.param = param
		self.body = body

	def toString(self):
		return ('(λ' + self.param + '.' + self.body.toString() + ')')

class Application():
	def __init__(self, lhs, rhs):
		self.rhs = rhs #right hand side of equation
		self.lhs = lhs #left hand side

	def toString(self):
		return self.lhs.toString() + self.rhs.toString()

class Identifier(): #aka variable
	def __init__(self, value, name):
		self.value = value
		self.name = name

	def toString(self):
		return self.name