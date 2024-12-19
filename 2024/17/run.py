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

# example:
#instrs = [0,3,5,4,3,0]

# Each loop iteration prints one number, which is only
# a function of the current lowest 3-bit chunk of A, plus
# a shift which might depend on the lowest four chunks of A.
# Thus the final iteration only depends on the highest chunk,
# the previous iteration on the two highest chunks, etc.,
# and we can start from the most significant chunk and
# iterate over possible solutions -- for each test value
# we check that outputs corresponding to the filled-in
# chunks of A are correct, since the last N outputs are
# fixed by the N most-significant chunks of A.
#
# Iterating over possible solutions starting from the
# most-significant chunk means the first solution found
# is the smallest.
#
# aa is a list of 3-bit chunks; A is aa[3]..aa[18]. We pad with 
# extra zeroes to make the shift logic easier.
aa = [0]*19
i = 3
while i < 19:
	# i is an index to the current chunk we're testing possible
	# values for: the more-significant chunks are assumed correct,
	# but if we can't find a solution we backtrack.
	possible = False
	for n in range(aa[i], 8):
		# check each possible value of this chunk
		shift = (n^7)
		# the output chunk, assuming this chunk and all higher ones
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
			aa[i] = n
			break
	if possible:
		# continue with next chunk
		i += 1
	else:
		# no solutions given earlier chunks, so we backtrack
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

# convert the chunks back into a single integer
result2 = sum(c<<(3*(18-i)) for (i,c) in enumerate(aa))

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=17)
