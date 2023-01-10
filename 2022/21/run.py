input_test = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

input = input_test
input = open("input.py").read()

def parse_line(l):
	dest, rest = l.split(":")
	rest = rest.strip()
	if " " not in rest:
		return dest, int(rest)
	a, op, b = rest.split(" ")
	return dest, (a,op,b, rest)

monkeys = [parse_line(l) for l in input.splitlines()]
known = dict((dest,val) for (dest,val) in monkeys if isinstance(val, int))
to_solve = [(dest,val) for (dest,val) in monkeys if not isinstance(val, int)]

remaining = to_solve
while remaining:
	nxt = []
	for monkey in remaining:
		dest, (a,op,b,s) = monkey
		if a in known and b in known:
			known[dest] = eval(s, known)
		else:
			nxt.append(monkey)
	remaining = nxt

print("Part 1:", int(known["root"]))

# part 2

known = dict((dest,val) for (dest,val) in monkeys if isinstance(val, int) and dest != "humn")
to_solve = [(dest,val) for (dest,val) in monkeys if not isinstance(val, int)]
unknown = set(["humn"])
exprs = {}

# solve what we can
remaining = to_solve
while remaining:
	nxt = []
	for monkey in remaining:
		dest, (a,op,b,s) = monkey
		if a in known and b in known:
			known[dest] = eval(s, known)
		elif a in unknown or b in unknown:
			unknown.add(dest)
			exprs[dest] = (a,op,b)
		else:
			nxt.append(monkey)
	remaining = nxt

def isnum(x):
	return isinstance(x, int) or isinstance(x, float)
	
# reduce exprs
def expand(a,op,b,exprs):
	l = a
	if l in known:
		l = known[l]
	if not isnum(l) and l != "humn":
		al,opl,bl = exprs[l]
		l = expand(al,opl,bl,exprs)
	r = b
	if r in known:
		r = known[r]
	if not isnum(r) and l != "humn":
		ar,opr,br = exprs[r]
		r = expand(ar,opr,br,exprs)
	return (l,op,r)

def do_op(a,op,b):
	return {
		"+": lambda x,y:x+y,
		"-": lambda x,y:x-y,
		"*": lambda x,y:x*y,
		"/": lambda x,y:x/y,
	}[op](a,b)

def distribute_times(x,y):
	if isnum(x):
		if y == "humn":
			return (x,"*",y)
		ay,opy,by = y
		if opy in ["+", "-"]:
			a = x*ay if isnum(ay) else (x,"*",ay)
			b = x*by if isnum(by) else (x,"*",by)
			return (a,opy,b)
		else:
			return ((x,"*",ay),opy,by)
	elif isnum(y):
		return distribute_times(y,x)
	# if you want to handle this case, file a FOIL request
	return (x,"*",y)

# very ad hoc and incomplete set of algebraic simplifications, just enough to solve my input data
def simplify(expr):
	if expr == "humn":
		return expr
	if isnum(expr):
		return expr
	a,op,b = expr
	a = simplify(a)
	b = simplify(b)
	if isnum(a) and isnum(b):
		return do_op(a,op,b)
	if op == "*":
		return distribute_times(a,b)
	if op in ["+", "-"]:
		if isnum(a) or isnum(b):
			if op == "-" and isnum(a):
				# not this case
				return (a,op,b)
			i, x = (a,b) if isnum(a) else (b,a)
			if x == "humn":
				return (a,op,b)
			# try combining int with sub-exprs
			ax,opx,bx = x
			if opx in ["+", "-"]:
				axi = (ax,op,i)
				axi_simple = simplify(axi)
				if axi_simple != axi:
					return (axi_simple, opx, bx)
				bxi = (bx,op,i if opx == "+" else -i)
				bxi_simple = simplify(bxi)
				if bxi_simple != bxi:
					return (ax, opx, bxi_simple)
					
	if op == "==" and isnum(b) and a != "humn":
		ax,opx,bx = a
		if opx == "/" and isnum(bx):
			return (ax,"==",bx*b)
		if opx == "-" and isnum(bx):
			return (ax,"==",bx+b)
		if opx == "-" and isnum(ax):
			return (bx,"==",ax-b)
		if opx == "+" and isnum(bx):
			return (ax,"==",b-bx)
		if opx == "+" and isnum(ax):
			return (bx,"==",b-ax)
		# terminal case
		if isnum(ax) and opx == "*" and bx == "humn":
			return ("humn","==",b/ax)
				
	return (a,op,b)

a,_,b = exprs["root"]
expr = expand(a,"==",b,exprs)

before = expr
after = simplify(before)
while after != before:
	before = after
	after = simplify(before)

a,op,b = after
assert(a == "humn" and op == "==" and int(b) == b)
print("Part 2:", int(b))

	

		
