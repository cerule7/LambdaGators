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
	print("VISITING " + node.toString())
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
		return recursive_reduce(term)

def checkGrammar(source):
    #check parens matching
    s = list()
    balanced = True
    index = 0
    temp = [x for x in source if x == '(' or x == ')']
    while index < len(temp) and balanced:
    	c = temp[index]
    	if c == '(':
    		s.append(c)
    	else:
    		if len(s) == 0:
    			balanced = False
    		else:
    			s.pop()
    	index += 1
    #correct lambda and dot placement 
    print(len(source))
    if len(source) == 1 and (source[0] == '\\' or source[0] == 'λ' or source[0] == '.'):
    	return False
    for i in range(0, len(source) - 1):
    	if source[i] == '\\' or source[i] == 'λ' or source[i] == '.':
    		if source[i] == '.':
	    		if i + 1 < len(source) - 1 and source[i + 1] not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
	    			return False
	    	else:
	    		b = False
	    		for j in range(i + 1, len(source) - 1):
	    			if j == '.':
	    				b = True
	    		if not b:
	    			return False
    return (balanced and len(s) == 0)

def main():
	first = input("Enter lambda calculus here:")
	source = ""
	for c in first:
		if c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\\.()λ ':
			source = source + c
		else:
			print("Unsupported characters")
			return
	source = [p for p in source if p != ' ']
	if not checkGrammar(source):
		print("Incorrect syntax")
	else:
		lexer = Lexer(source)
		lexer.token = lexer.nextToken()
		parser = lambda_parser.Parser(lexer)
		ast = parser.parse()
		i = input("Type n to continue or q to end: ")
		while(i != 'q'):
			ast = betareduce(ast)
			nodelist = genNodeList(ast, [])
			print("REDUCED TERM: " + ast.toString())
			print("NODES IN TERM: ")
			print([n.toString() for n in nodelist])
			i = input("Type n to continue or q to end: ")
		print("FINAL REDUCTION: " + ast.toString())

def genNodeList(node, nodelist):
	if isinstance(node, AST.Identifier) or isinstance(node, AST.Abstraction):
		nodelist.append(node)
	elif isinstance(node, AST.Application):
		nodelist = genNodeList(node.lhs, nodelist)
		nodelist = genNodeList(node.rhs, nodelist)
	return nodelist


main()