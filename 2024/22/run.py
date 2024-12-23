from me import *

input = get_data_2024(22)

input = input_test

nums = lmap(int, input.splitlines())

mask = (1<<24) - 1

def step(n):
	n2 = ((n<<6) ^ n) & mask
	n3 = ((n2>>5) ^ n2) & mask
	return ((n3<<11) ^ n3) & mask

def stepn(x, n):
	for i in range(n):
		x = step(x)
	return x
	
# Part 1

result1 = sum(stepn(x, 2000) for x in nums)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=22)

# Part 2

# lol, overkill
class RingBuf(object):
	def __init__(self, vals):
		self.buf = list(vals)
		self.head = 0
		self.N = len(vals)
	
	def push(self, val):
		self.buf[self.head] = val
		self.head = (self.head+1)%4
	
	def __iter__(self):
		for i in range(self.N):
			yield self.buf[(self.head+i)%self.N]

def seq_num(deltas):
	# take a sequence of 4 numbers in [-9,9]
	# and represent as a single number in base 19
	return sum((d+9)*(19**i) for (i,d) in enumerate(deltas))

def decode_seq(n):
	# only need this for debugging
	deltas = []
	for i in range(4):
		n, dig = n//19, n%19
		deltas.append(dig-9)
	return deltas

def price_seqs(s0, steps):
	# do the first four steps by hand to make the
	# loop a little easier
	s1 = step(s0)
	s2 = step(s1)
	s3 = step(s2)
	s4 = step(s3)
	
	ps = [s%10 for s in (s0,s1,s2,s3,s4)]
	deltas = RingBuf([ps[i]-ps[i-1] for i in range(1,5)])
	seqs = {seq_num(deltas): ps[4]}
	
	s = s4
	p = ps[4]
	for i in range(steps-4):
		s = step(s)
		pnew = s%10
		deltas.push(pnew-p)
		p = pnew
		sn = seq_num(deltas)
		if sn not in seqs:
			seqs[sn] = pnew
		
	return seqs

totals = [0]*(19**4)

# part 2 example, yields 23
#nums = [1,2,3,2024]

for s in nums:
	seqs = price_seqs(s, 2000)
	for (sn, p) in seqs.items():
		totals[sn] += p

result2 = max(totals)
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=22)
