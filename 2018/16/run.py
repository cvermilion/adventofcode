def ops(m):
	return {
		"addr": lambda a,b: m.reg[a]+m.reg[b],
		"addi": lambda a,b: m.reg[a]+b,
		"mulr": lambda a,b: m.reg[a]*m.reg[b],
		"muli": lambda a,b: m.reg[a]*b,
		"banr": lambda a,b: m.reg[a]&m.reg[b],
		"bani": lambda a,b: m.reg[a]&b,
		"borr": lambda a,b: m.reg[a]|m.reg[b],
		"bori": lambda a,b: m.reg[a]|b,
		"setr": lambda a,b: m.reg[a],
		"seti": lambda a,b: a,
		"gtir": lambda a,b: 1 if a>m.reg[b] else 0,
		"gtri": lambda a,b: 1 if m.reg[a]>b else 0,
		"gtrr": lambda a,b: 1 if m.reg[a]>m.reg[b] else 0,
		"eqir": lambda a,b: 1 if a==m.reg[b] else 0,
		"eqri": lambda a,b: 1 if m.reg[a]==b else 0,
		"eqrr": lambda a,b: 1 if m.reg[a]==m.reg[b] else 0,
	}

class Machine (object):
	def __init__(self):
		self.reg = [0,0,0,0]
		self.ops = ops(self)
	
	def reset(self):
		self.reg = [0,0,0,0]
	
	def exe(self, op, a, b, c):
		self.reg[c] = self.ops[op](a,b)

m = Machine()

m.exe("eqrr", 0,1,2)
print(m.reg)

from parse import parse
exes = open("examples.txt").read().split("\n\n")
print(exes[0])
fmt = """Before: [{:d}, {:d}, {:d}, {:d}]
{:d} {:d} {:d} {:d}
After:  [{:d}, {:d}, {:d}, {:d}]"""
exe_data = [parse(fmt, e) for e in exes]
print(exe_data[-2])

count=0
possible_names = dict((i,set(m.ops.keys())) for i in range(16))
for (ii,data) in enumerate(exe_data[:-1]):
	r1 = [data[i] for i in range(4)]
	r2 = [data[i] for i in range(8,12)]
	op,a,b,c = [data[i] for i in range(4,8)]
	
	valid=0
	oo = []
	for opname in m.ops:
		m.reg = r1[:]
		m.exe(opname, a, b, c)
		if m.reg == r2:
			oo.append(opname)
			valid += 1
	
	if valid >= 3:
		count += 1
		#print(ii,valid,"sols for", r1,r2,op,a,b,c,oo)
	
	possible_names[op].intersection_update(set(oo))

print(count)
print(possible_names)

resolved = {}

possible_codes = dict((n, set()) for n in m.ops.keys())
for op, poss in possible_names.items():
	for p in poss:
		possible_codes[p].add(op)

print(possible_codes)

while len(resolved) < 16:
	for op, poss in possible_names.items():
		if len(poss) == 1:
			resolved[op] = poss.pop()
	for name, poss in possible_codes.items():
		if len(poss) == 1:
			op = poss.pop()
			resolved[op] = name
	for op, name in resolved.items():
		if op in possible_names:
			del possible_names[op]
		if name in possible_codes:
			del possible_codes[name]
	for poss in possible_names.values():
		poss.difference_update(set(resolved.values()))
	for poss in possible_codes.values():
		poss.difference_update(set(resolved.keys()))

print(resolved)

input = open("input.txt").read().splitlines()
fmt = "{:d} {:d} {:d} {:d}"
cmds = [parse(fmt,l) for l in input]

m.reset()
for (op, a, b, c) in cmds:
	m.exe(resolved[op], a, b, c)
print(m.reg)
