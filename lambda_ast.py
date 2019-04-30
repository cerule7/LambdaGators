class Abstraction():
	def __init__(self, param, body):
		self.param = param
		self.body = body

	def __str__(self):
		return ('λ' + self.param + '.' + self.body)

class Application():
	def __init__(self, lhs, rhs):
		self.rhs = rhs
		self.lhs = lhs

	def __str__(self):
		return str(self.lhs) + " " + str(self.rhs)

class Identifier():
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return self.value