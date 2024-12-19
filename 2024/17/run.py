from me import *

input = get_data_2024(17)

#input = input_test

def parse_prog(s):
	lines = s.splitlines()
	A,B,C = (parse("Register {}: {:d}", lines[i])[1] for i in range(3))
	instrs = lmap(int, lines[4].split(": ")[1].split(","))
	return A,B,C,instrs

# Part 1

class CPU(object):
	def __init__(self, A, B, C):
		self.regs = [0,1,2,3,A,B,C]
		self.pc = 0
		self.buf = []

	def adv(self, ope):
		self.regs[4] >>= self.regs[ope]
	
	def bdv(self, ope):
		self.regs[5] = self.regs[4] >> self.regs[ope]
	
	def cdv(self, ope):
		self.regs[6] = self.regs[4] >> self.regs[ope]
	
	def bxl(self, ope):
		self.regs[5] ^= ope
	
	def bxc(self, _ope):
		self.regs[5] ^= self.regs[6]
		
	def bst(self, ope):
		self.regs[5] = self.regs[ope] & 7
	
	def jnz(self, ope):
		if self.regs[4] != 0:
			self.pc = ope-2 # account for increment afterward
	
	def out(self, ope):
		self.buf.append(self.regs[ope] & 7)
	
	def step(self, instrs):
		opc, ope = instrs[self.pc:self.pc+2]
		[self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv][opc](ope)
		self.pc += 2

	def run(self, instrs):
		while self.pc < len(instrs):
			self.step(instrs)
		return ",".join(lmap(str, self.buf))
	
A,B,C,instrs = parse_prog(input)
cpu = CPU(A,B,C)

result1 = cpu.run(instrs)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=17)

# Part 2

#instrs = [0,3,5,4,3,0]

def run(a):
	cpu = CPU(a,0,0)
	return cpu.run(instrs)

def try_quine(a):
	cpu = CPU(a,0,0)
	while cpu.pc < len(instrs):
		cpu.step(instrs)
		if len(cpu.buf) > len(instrs):
			return False
		if cpu.buf != instrs[:len(cpu.buf)]:
			return False
	return cpu.buf == instrs

def try_quine2(a, i):
	next_out = 7 & (3 ^ (a&7) ^ (a >> ((a&7)^7)))
	if next_out != instrs[i]:
		return False
	return try_quine2(a>>3, i+1)

def makeA(aa):
	return sum(c<<(3*(18-i)) for (i,c) in enumerate(aa))
	
# we know because the program has a single while
# loop and shifts A 3 bits each time that A
# has len(instrs)*3 bits (highest 2 might be zero)
# pad with 3 extra chunks to make the shift test easier; highest nonzero bit of A is in i=3
aa = [0]*19
i = 3
while i < 19:
	# find the smallest solution by just iterating
	# over possible 3-bit chunks of A
	# starting at MSB
	possible = False
	print("i=",i,aa[:i+1])
	for n in range(aa[i], 8):
		# check each value of this chunk
		shift = (n^7)
		out = 7&(
			(3 ^ n) ^
			(
				(n + 
				 (aa[i-1]<<3) +
				 (aa[i-2]<<6) + 
				 (aa[i-3]<<9)
				)>>shift
			)
		)
		if instrs[15-(i-3)] == out:
			possible = True
			print("possible val",n)
			aa[i] = n
			break
	if possible:
		# continue with next chunk
		i += 1
	else:
		# no solutions given earlier chunks
		print("oops, go back", aa[:i+1])
		aa[i] = 0
		i -= 1
		while aa[i] == 7 and i >= 0:
			aa[i] = 0
			i -= 1
			
		if i < 3:
			# no solutions at all!
			assert(False)
		# loop at i again but start with the next value
		aa[i] += 1


print("aa chunks", aa)
result2 = sum(c<<(3*(18-i)) for (i,c) in enumerate(aa))

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=17)
