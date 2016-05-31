import ast



class Walker(ast.NodeVisitor):
	def generic_visit(self, node):
		print("Generic:", type(node).__name__)
		super().generic_visit(node)

	def visit_ClassDef(self, node):
		print("Visit Class:", type(node).__name__)
		#ast.NodeVisitor.generic_visit(self, node)



if __name__ == '__main__':
	w = Walker()

	with open("test.py") as f:
		c = f.read()
		a = ast.parse(c)
		w.visit(a)