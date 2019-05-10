import lambda_ast as AST

class Parser():
	def __init__(self, lexer):
		self.lexer = lexer
		self.varlist = list() #this is where all variables are stored

	def term(self):
		#if current token is a lambda, find parameter and add to varlist
		if(self.lexer.skip('LAMBDA', self.lexer.token)):
			x = self.lexer.assertType('VAR', self.lexer.token)
			self.lexer.match('PERIOD', self.lexer.token)
			self.varlist.append(x)
			term = self.term()
			return AST.Abstraction(x, term)
		else:
			return self.application()

	def parse(self):
		result = self.term()
		print(self.varlist)
		self.lexer.match('EOF', self.lexer.token)
		return result

	def application(self): #for making applications
		lhs = self.atom()
		while(True):
			rhs = self.atom() #find right hand side of application
			if rhs is None:
				return lhs
			else:
				lhs = AST.Application(lhs, rhs)

	def atom(self):
		#if ( then create a lambda application and continue until )
		if(self.lexer.skip('LPAREN', self.lexer.token)):
			term = self.term()
			self.lexer.match('RPAREN', self.lexer.token)
			return term
		elif(self.lexer.typeMatches('VAR')): #if variable add to varlist
			x = self.lexer.assertType('VAR', self.lexer.token)
			if x not in self.varlist:
				self.varlist.append(x)
			return AST.Identifier(self.varlist.index(x), x)
		else:
			return None
