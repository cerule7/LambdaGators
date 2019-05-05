import lambda_ast as AST
import lambda_parser

class Token():
	def __init__(self, toktype, value):
		self.type = toktype #EOF, LAMBDA, LPAREN, RPAREN, LCID, PERIOD
		self.value = value

	def toString(self):
		return "TOKEN TYPE: " + self.type + " VALUE: " + self.value

class Lexer():
	def __init__(self, inp):
		self.input = inp
		self.index = 0
		self.token = None

	def nextToken(self):
		inp = self.input
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
		elif((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')):
			return Token('VAR', c)	
		else:
			return "Error: unsupported character"	

	def typeMatches(self, toktype):
		return (self.token.type == toktype)

	def skip(self, toktype, token):
		if (token.type == toktype):
			self.token = self.nextToken()
			return True
		else:
			return False

	def assertType(self, toktype, token):
		if(token.type != toktype):
			return self.token.value
		else:
			newtok = self.token
			self.match(toktype, newtok)
			return newtok.value

	def match(self, toktype, token):
		if(self.typeMatches(toktype)):
			self.token = self.nextToken()
			return True
		else:
			return False

def isValue(node):
	return isinstance(node, AST.Abstraction)

# # #goes one step at a time (hopefully)
# def eval(node):
# 	if isinstance(node, AST.Application()):
# 		if isValue(node.lhs) and isValue(node.rhs):
# 			node = substitute(node.rhs, node.lhs.body)
# 		elif isValue(node.lhs):
# 			node.rhs = eval(node.rhs)
# 		else:
# 			node.lhs = eval(node.lhs)
# 	elif isValue(node):
# 		return node

# def traverse(node, index):


# def shift(x, node): #shift all free vars in node by x
	
	
# def depth(value, node, depth):
# 	if isinstance(node, AST.Application()):
# 		return AST.Application(aux(value, node.lhs, depth), aux(value, node.rhs, depth))
# 	elif isinstance(node, AST.Abstraction()):
# 		return AST.Abstraction(node.param, aux(value, abs.body, depth + 1))
# 	elif isinstance(node, AST.Identifier()):
# 		if(depth == node.value):
# 			return shift(depth, value)
# 		else:
# 			return node

# def aux(value, node, depth):
# 	traverse(depth(value, node, depth))

# def subst(value, node):
# 	return aux(value, node, 0)

# def substitute(value, node): #substitute all vars in node w a dbi of 0 by value
# 	return shift(-1, subst(shift(1, value), node))

def recursive_sub(old, new, node):
	print('OLD ' + old.toString())
	print("NEW " + new.toString())
	print("NODE "  + node)
	if isinstance(old, AST.Identifier) and old.name == node:
			print("RETURNED " + new.toString())
			return new
	elif isinstance(old, AST.Application):
		old.lhs = recursive_sub(old.lhs, new, node)
		old.rhs = recursive_sub(old.rhs, new, node)
	elif isinstance(old, AST.Abstraction):
		if old.param == node:
			print("SAME NAME")
			old.param = recursive_sub(old.param, new, node)
		print(old.body + " " + new.toString())
		old.body = recursive_sub(old.body, new, node)
	print("RETURNED OLD AS " + old.toString())
	return old 

def recursive_reduce(node):
	if isinstance(node, AST.Identifier) or isinstance(node, AST.Abstraction):
		return node
	elif isinstance(node, AST.Application):
		print("CURRENT NODE " + node.toString())
		if isinstance(node.lhs, AST.Abstraction):
			return recursive_sub(node.lhs.body, node.rhs, node.lhs.param)
		else:
			newlhs = recursive_reduce(node.lhs)
			if newlhs != node.lhs:
				node.lhs = newlhs
				print("NEW LHS " + node.lhs.toString())
				return node
			else:
				node.rhs = recursive_reduce(node.rhs)
				print("NEW RHS " + node.rhs.toString())
				return node

def betareduce(term):
	if isinstance(term, AST.Identifier) or isinstance(term, AST.Abstraction):
		return term
	elif isinstance(term, AST.Application):
		temp = term
		while(True):
			term_str = temp.toString()
			print("TERM STR " + term_str)
			reduced = recursive_reduce(temp)
			print("REDUCED " + reduced.toString())
			if term_str == reduced.toString():
				return temp
			else:
				temp = reduced

def main():
	source = input("Enter lambda calculus here:")
	source = [x for x in source if x != ' '] #strip whitespace
	lexer = Lexer(source)
	lexer.token = lexer.nextToken()
	parser = lambda_parser.Parser(lexer)
	ast = parser.parse()
	print(ast.lhs.toString())
	print(ast.rhs.toString())
	print(betareduce(ast).toString())

main()