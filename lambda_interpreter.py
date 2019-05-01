import lambda_ast as AST
import lambda_parser

class Token():
	def __init__(self, toktype, value):
		self.type = toktype #EOF, LAMBDA, LPAREN, RPAREN, LCID, PERIOD
		self.value = value

class Lexer():
	def __init__(self, inp):
		self.input = inp
		self.index = 0
		self.token = nextToken(self, self.input)

	def nextToken(self, inp):
		if self.index >= len(inp):
			return Token('EOF', 'none')
		c = inp[self.index]
		self.index += 1
		if(c == '\\' or c == 'λ:'):
			return Token('LAMBDA', 'none')
		elif(c == '.'):
			return Token('PERIOD', 'none')
		elif(c == '('):
			return Token('LPAREN', 'none')
		elif(c == ')'):
			return Token('RPAREN', 'none')
		elif((c <= 'a' and c >= 'z') or (c <= 'A' and c >= 'Z')):
			return Token('LCID', c)	
		else:
			return "Error: unsupported character"	

	def next(toktype, token):
		return (token.type == toktype)

	def skip(self, toktype, token):
		if (token.type == toktype):
			self.token = nextToken(self, self.input)
			return True
		else:
			return False

	def assertType(self, toktype, token):
		if(token.type != toktype):
			return token.value
		else:
			newtok = nextToken(self, self.input)
			value = match(self, toktype, newtok)
			return value

	def match(self, toktype, token):
		if(next(toktype, token)):
			self.token = nextToken(self, self.input)
			return True
		else:
			return False

def isValue(node):
	return isinstance(node, AST.Abstraction())

#goes one step at a time (hopefully)
def eval(node):
	if isinstance(node, AST.Application()):
		if isValue(node.lhs) and isValue(node.rhs):
			node = substitute(node.rhs, node.lhs.body)
		elif isValue(node.lhs):
			node.rhs = eval(node.rhs)
		else:
			node.lhs = eval(node.lhs)
	elif isValue(node):
		return node

def traverse(node, index):


def shift(x, node): #shift all free vars in node by x
	
	

def substitute(value, node): #substitute all vars in node w a dbi of 0 by value
	return shift(-1, substitute(shift(1, value), node))

def main():
	source = input("Enter lambda calculus here:")
	lexer = Lexer()
	parser = lambda_parser.Parser(lexer)
	ast = parser.parse()