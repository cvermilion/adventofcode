from functools import reduce
from operator import xor
text="31,2,85,1,80,109,35,63,98,255,0,13,105,254,128,33"

class CircularList (object):
	def __init__(self, l):
		self.l = l
	
	def slice(self, i,j):
		s = list(range(j-i))
		for k in range(i, j):
			s[k-i] = self.l[k % len(self.l)]
		return s
	
	def replace(self, i, s):
		for k, x in enumerate(s):
			self.l[(i+k)%len(self.l)] = x

l = CircularList(list(range(256)))

def do_round(l, lengths, cur, skip):
	for length in lengths:
		s = l.slice(cur, cur+length)
		s.reverse()
		l.replace(cur, s)
		cur += length+skip
		skip+=1
	return cur, skip

lengths = map(int, text.split(","))
do_round(l, lengths, 0, 0)
print(l.l[0]*l.l[1])

def knot_hash(text):
	extra_lengths = [17, 31, 73, 47, 23]
	byte_lengths = list(map(ord, text)) + extra_lengths

	sparse = CircularList(list(range(256)))
	cur, skip = 0, 0
	for i in range(64):
		cur, skip = do_round(sparse, byte_lengths, cur, skip)
	dense = [reduce(xor, sparse.slice(16*i, 16*(i+1))) for i in range(16)]
	return ''.join('{:02x}'.format(b) for b in dense)

print(knot_hash(text))
