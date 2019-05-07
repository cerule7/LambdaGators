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
		if(c == '\\' or c == 'λ'):
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

def recursive_sub(old, new, node):
	if isinstance(old, AST.Identifier) and old.name == node:
			return new
	elif isinstance(old, AST.Application):
		old.lhs = recursive_sub(old.lhs, new, node)
		old.rhs = recursive_sub(old.rhs, new, node)
	elif isinstance(old, AST.Abstraction):
		if old.param == node:
			old.param = recursive_sub(old.param, new, node)
		old.body = recursive_sub(old.body, new, node)
	return old 

def recursive_reduce(node):
	if isinstance(node, AST.Identifier) or isinstance(node, AST.Abstraction):
		return node
	elif isinstance(node, AST.Application):
		if isinstance(node.lhs, AST.Abstraction):
			return recursive_sub(node.lhs.body, node.rhs, node.lhs.param)
		else:
			newlhs = recursive_reduce(node.lhs)
			if newlhs != node.lhs:
				node.lhs = newlhs
				return node
			else:
				node.rhs = recursive_reduce(node.rhs)
				return node

def betareduce(term):
	if isinstance(term, AST.Identifier) or isinstance(term, AST.Abstraction):
		return term
	elif isinstance(term, AST.Application):
		temp = term
		while(True):
			term_str = temp.toString()
			reduced = recursive_reduce(temp)
			if term_str == reduced.toString():
				return temp
			else:
				temp = reduced

def checkGrammar(source):
    #check parens matching
    s = list()
    balanced = True
    index = 0
    source = [x for x in source if x == '(' or x == ')']
    while index < len(source) and balanced:
    	c = source[index]
    	if c == '(':
    		s.append(c)
    	else:
    		if len(s) == 0:
    			balanced = False
    		else: 
    			s.pop()
    	index += 1
    return (balanced and len(s) == 0)

def main():
	while(True):
		first = input("Enter lambda calculus here:")
		source = [x for x in first if x in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\\.()']
		if first != source:
			print("Error: Unsupported characters")
		elif not checkGrammar(source):
			print("Unbalanced parentheses")
		else:
			lexer = Lexer(source)
			lexer.token = lexer.nextToken()
			parser = lambda_parser.Parser(lexer)
			ast = parser.parse()
			print("FINAL REDUCTION: " + betareduce(ast).toString())

main()