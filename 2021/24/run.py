data = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""

data = open("input.py").read()

ops = [l.split() for l in data.splitlines()]

def val(reg, b):
	if b in reg:
		return reg[b]
	return int(b)

def execute(reg, input, op):
	if op[0] == "inp":
		reg[op[1]] = input.pop()
		return
	code, a, b = op
	reg[a] = {
		"add": lambda x,y: x+y,
		"mul": lambda x,y: x*y,
		"div": lambda x,y: int(x/y),
		"mod": lambda x,y: x%y,
		"eql": lambda x,y: 1 if x==y else 0,
	}[code](reg[a], val(reg, b))

class Inp(object):
	def __init__(self, n):
		self.n = n
	def __repr__(self):
		return "Inp<{}>".format(self.n)
	def str(self, t):
		return ("  " * t) + repr(self)
	def __eq__(self, x):
		return isinstance(x, Inp) and self.n == x.n
	def min(self):
		return 1
	def max(self):
		return 9
		
class Val(object):
	def __init__(self, v):
		self.val = v
	def __repr__(self):
		return str(self.val)
	def str(self, t):
		return ("  " * t) + str(self.val)
	def __eq__(self, x):
		return isinstance(x, Val) and self.val == x.val
	def min(self):
		return self.val
	def max(self):
		return self.val
		

class Op(object):
	def __init__(self, op, a, b):
		self.op = op
		self.a = a
		self.b = b
		self.distributed = False # used in simplifying mod ops
	def __repr__(self):
		return "[{}, {}, {}]".format(self.op, self.a, self.b)
	def str(self, t):
		if not isinstance(self.a, Op) and not isinstance(self.b, Op):
			return "  "*t + repr(self)
		return ("  " * t) + "[" + self.op + "\n" + self.a.str(t+1) + "\n" + self.b.str(t+1) + "\n" + ("  " * t) + "]"
	def __eq__(self, x):
		if not isinstance(x, Op) or x.op != self.op:
			return False
		return self.a == x.a and self.b == x.b
	def min(self):
		if self.op == "add":
			return self.a.min() + self.b.min()
		if self.op == "mul":
			if self.a.min() >= 0 and self.b.min() >= 0:
				return self.a.min() * self.b.min()
			# could do better?
			return -max([abs(self.a.max()), abs(self.a.min())]) * max([abs(self.b.max()), abs(self.b.min())])
		if self.op == "div":
			# could do better than this
			return -abs(self.a.max())
		if self.op == "mod":
			return 0
		if self.op == "eql":
			return 0
	def max(self):
		if self.op == "add":
			return self.a.max() + self.b.max()
		if self.op == "mul":
				return max([abs(self.a.max()), abs(self.a.min())]) * max([abs(self.b.max()), abs(self.b.min())])
		if self.op == "div":
			# could do better than this
			return max([abs(self.a.max()), abs(self.a.min())])
		if self.op == "mod":
			return max([self.b.max(), 0])
		if self.op == "eql":
			return 1

class Test(object):
	# representation of a common expression type in the input:
	# (in_i + n != in_j)
	# These appear a lot and can only take the values 0 or 1, so we track them specially.
	def __init__(self, i, n, j):
		self.i = i
		self.n = n
		self.j = j
	def __repr__(self):
		return "c{}{}".format(self.i, self.j)
	def __eq__(self, x):
		return isinstance(x, Test) and (self.i,self.n,self.j) == (x.i,x.n,x.j)
	def str(self, t):
		return "  "*t + repr(self)
	def expr(self):
		return Op("eql", Op("eql", Op("add", Inp(self.i), Val(self.n)), Inp(self.j)), Val(0))
	def min(self):
		return 0
	def max(self):
		return 1
		
# could make this generic by recognizing this pattern in the input
consts = [Test(2,8,3), Test(3,-6,4), Test(1,-2,4), Test(5,-8,6), Test(0, 2, 7), Test(9, -6, 10), Test(11,-1,12), Test(8,-4,13)]

def simplify(expr):
	# apply a ton of algebraic simplifications
	if not isinstance(expr, Op):
		return expr
	a,b = expr.a, expr.b
	
	if expr.op == "add":
		if isinstance(expr.a, Val) and isinstance(expr.b, Val):
			return Val(expr.a.val + expr.b.val)
		if isinstance(expr.a, Val) and expr.a.val == 0:
			return expr.b
		if isinstance(expr.b, Val) and expr.b.val == 0:
			return expr.a
		x,y = (a,b) if isinstance(a, Val) else (b,a)
		if isinstance(x, Val) and isinstance(y, Op) and y.op == "add":
			xx,yy = (y.a, y.b) if isinstance(y.a, Val) else (y.b, y.a)
			if isinstance(xx, Val):
				return simplify(Op("add", yy, Val(x.val+xx.val)))
		return expr
	if expr.op == "mul":
		if isinstance(expr.a, Val) and isinstance(expr.b, Val):
			return Val(expr.a.val * expr.b.val)
		if (isinstance(expr.a, Val) and expr.a.val == 0) or (isinstance(expr.b, Val) and expr.b.val == 0):
			return Val(0)
		if isinstance(expr.a, Val) and expr.a.val == 1:
			return expr.b
		if isinstance(expr.b, Val) and expr.b.val == 1:
			return expr.a
		return expr
	if expr.op == "div":
		if isinstance(expr.a, Val) and isinstance(expr.b, Val):
			return Val(int(expr.a.val / expr.b.val))
		if isinstance(expr.a, Val) and expr.a.val == 0:
			return Val(0)
		if isinstance(expr.b, Val) and expr.b.val == 1:
			return expr.a
		if a.max() < b.min():
			return Val(0)
		if isinstance(a, Op) and a.op == "add" and isinstance(b, Val):
			# (a*x + y)/a = x + y/a
			if isinstance(a.a, Op) and a.a.op == "mul":
				if isinstance(a.a.a, Val) and a.a.a.val == b.val:
					return simplify(Op("add", a.a.b, simplify(Op("div", a.b, b))))
				if isinstance(a.a.b, Val) and a.a.b.val == b.val:
					return simplify(Op("add", a.a.a, simplify(Op("div", a.b, b))))
			if isinstance(a.b, Op) and a.b.op == "mul":
				if isinstance(a.b.a, Val) and a.b.a.val == b.val:
					return simplify(Op("add", a.b.b, simplify(Op("div", a.a, b))))
				if isinstance(a.b.b, Val) and a.b.b.val == b.val:
					return simplify(Op("add", a.b.a, simplify(Op("div", a.a, b))))
		return expr
	if expr.op == "mod":
		if isinstance(expr.a, Val) and isinstance(expr.b, Val):
			return Val(expr.a.val % expr.b.val)
		if isinstance(expr.a, Val) and expr.a.val == 0:
			return Val(0)
		if expr.a.max() < expr.b.min() and expr.b.min() > 0:
			return expr.a
		if isinstance(expr.b, Val) and isinstance(expr.a, Op) and expr.a.op == "mul":
			if (isinstance(expr.a.a, Val) and expr.a.a.val == expr.b.val) or (isinstance(expr.a.b, Val) and expr.a.b.val == expr.b.val):
				# (n * x) % n == 0
				return Val(0)
		if not expr.distributed and isinstance(expr.b, Val) and isinstance(expr.a, Op) and expr.a.op == "add":
			# (a + b) % n == (a%n + b%n) % n
			arm1 = Op("mod", expr.a.a, expr.b)
			arm1s = simplify(arm1)
			arm2 = Op("mod", expr.a.b, expr.b)
			arm2s = simplify(arm2)
			simpler = (arm1s != arm1) or (arm2s != arm2)
			if simpler:
				top = Op("mod", simplify(Op("add", arm1s, arm2s)), b)
				top.distributed = True
				return simplify(top)
		return expr
	if expr.op == "eql":
		if isinstance(expr.a, Val) and isinstance(expr.b, Val):
			return Val(1 if (expr.a.val == expr.b.val) else 0)
		x,y = (expr.a, expr.b) if isinstance(expr.a, Val) else (expr.b, expr.a)
		if isinstance(x, Val) and isinstance(y, Inp) and (x.val < 1 or x.val > 9):
			return Val(0)
		if isinstance(x, Val) and isinstance(y, Op) and y.op == "eql" and (x.val not in [0,1]):
			return Val(0)
		if expr.a.min() > expr.b.max() or expr.b.min() > expr.a.max():
			return Val(0)
		# special constants
		for c in consts:
			if expr == c.expr():
				return c
		return expr

def withSpecialVal(expr, c, n):
	if expr == c:
		return Val(n)
	if not isinstance(expr, Op):
		return expr
	return simplify(Op(expr.op, simplify(withSpecialVal(expr.a, c, n)), simplify(withSpecialVal(expr.b, c, n))))
	
def subs(expr, vals):
	for (c,v) in zip(consts, vals):
		expr = withSpecialVal(expr, c, v)
	return expr

def sub_vals():
	v = [[]]
	for c in consts:
		v = [l + [0] for l in v] + [l + [1] for l in v]
	return v

def run(ops, input):
	reg = {"w":0, "x":0, "y":0, "z":0}
	input = list(reversed(input))
	for o in ops:
		execute(reg, input, o)
	return reg

def run_expr(ops):
	reg = {"w":Val(0), "x":Val(0), "y":Val(0), "z":Val(0)}
	input = list(reversed([Inp(i) for i in range(14)]))
	for o in ops:
		if o[0] == "inp":
			reg[o[1]] = input.pop()
		else:
			b = o[2]
			if b in reg:
				b = reg[b]
			else:
				b = Val(int(b))
			reg[o[1]] = simplify(Op(o[0], reg[o[1]], b))
	return reg

def valid(n):
	input = map(int, str(n))
	return run(ops, input)["z"] == 0

def thru(n):
	return run_expr(ops[:n])

def check(expr, vals):
	z = subs(expr["z"], vals)
	return z.min() <= 0 and z.max() >= 0

out = run_expr(ops)
possible = [v for v in sub_vals() if check(out, v)]

# only two possible sets of Cxy values, this fixes most of the digits. Note that in those two cases the output value is fixed to zero but in the others it's (at least sometimes) a non-constant expression that can't be zero

# largest: 79197919993985
# smallest: 13191913571211


