ipreg = 1
input = open("input.txt").readlines()

# copied from day 16

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
	def __init__(self, instrs, ipreg):
		self.reg = [0,0,0,0,0,0]
		self.ops = ops(self)
		self.instrs = instrs
		self.ipreg = ipreg
	
	def reset(self):
		self.reg = [0,0,0,0,0,0]
	
	def exe(self, op, a, b, c):
		self.reg[c] = self.ops[op](a,b)
	
	def run(self):
		ip = self.reg[self.ipreg]
		i = 0
		while ip >= 0 and ip < len(self.instrs):
			i+=1
			instr = self.instrs[ip]
			op,a,b,c = instr
			self.reg[c] = self.ops[op](a,b)
			self.reg[self.ipreg] += 1
			if c == 0:
				print("setting 0", ip, m.reg)
			#if ip in [0, 25, 35]:
			#if c == self.ipreg:
				#print(i,"jumped",ip,"to",self.reg[self.ipreg], self.reg)
			ip = self.reg[self.ipreg]

fmt = "{} {:d} {:d} {:d}"
from parse import parse
# skip ip register line
instrs = [parse(fmt,l) for l in input[1:]]

# part 1
#m = Machine(instrs, ipreg)

# part 2
m = Machine(instrs, ipreg)
#m.reg[0] = 1

m.run()
print(m.reg)

