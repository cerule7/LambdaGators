import lambda_ast as AST

class Parser():
	def __init__(self, lexer):
		self.lexer = lexer

	def parse(self):
		result = term(self, [])
		self.lexer.match(self.lexer, 'EOF', self.lexer.token)
		return result

	def term(self, ctx):
		if(self.lexer.skip(self.lexer, 'LAMBDA', self.lexer.token)):
			x = self.lexer.assertType(self.lexer, 'LCID', self.lexer.token)
			self.lexer.match(self.lexer, 'PERIOD', self.lexer.token)
			term = term(self, [x].concat(ctx))
			return AST.Abstraction(x, term)
		else:
			return AST.Application(self, ctx)

	def application(self, ctx):
		lhs = self.atom(ctx)
		while(True):
			rhs = self.atom(ctx)
			if rhs is None:
				return lhs
			else:
				lhs = AST.Application(lhs, rhs)

	def atom(self, ctx):
		if(self.lexer.skip(self.lexer, 'LPAREN', self.lexer.token)):
			term = ctx
			self.lexer.match(self.lexer, 'RPAREN', self.lexer.token)
			return term
		elif(self.lexer.next(self.lexer, 'LCID', self.lexer.token)):
			x = self.lexer.assertType(self.lexer, 'LCID', self.lexer.token)
			return AST.Identifier(ctx.indexOf(x))
		else:
			return None