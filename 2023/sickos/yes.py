DONE = "DONE"

def apply(val, expr):
	"""Helper function for the | operator on pipeline below
	
	Examples:
	
Apply plain unary function
	
	apply("abc", list) => ["a", "b", "c"]
	
Map unary function over an iterable
	
	apply(["a", "b", "c"], [str.capitalize]) => ["A", "B", "C"]
	
Apply n-ary function with val as first arg
	
	apply("foobar", (str.replace, "o", "O")) => "fOObar"
	
Combine nesting and extra args
	
	apply(["a", "b", "c"], [(operator.add, "x")]) => ["ax", "bx", "cx"]
	
Deep nesting
	
	apply([[[1,2], [1,3]], [[4,2], [5,5]]]),[[[lambda x: x+1]]]) => [[[2, 3], [2, 4]], [[5, 3], [6, 6]]]
	"""
	if isinstance(expr, list):
			return [apply(elt, expr[0]) for elt in val]
	if isinstance(expr, tuple):
		f, *rest = expr
		return f(val, *rest)
	return expr(val)

class pipeline(object):
	def __init__(self, x):
		self.val = x
	
	def __or__(self, other):
		if other is DONE:
			return self.val
		return pipeline(apply(self.val, other))
	
