class Abstraction():
	def __init__(self, param, body):
		self.param = param
		self.body = body
		print(self.toString())

	def toString(self):
		return ('λ' + self.param + '.' + self.body.toString())

class Application():
	def __init__(self, lhs, rhs):
		self.rhs = rhs
		self.lhs = lhs
		print("APP MADE FOR " + self.rhs.toString() + " & " + self.lhs.toString())

	def toString(self):
		return "APP" + self.lhs.toString() + " " + self.rhs.toString()

class Identifier():
	def __init__(self, value, name):
		self.value = value
		self.name = name
		print("ID MADE FOR " + self.name)

	def toString(self):
		return self.name