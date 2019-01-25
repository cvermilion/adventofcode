input = open("input.txt").read().strip().split(" ")
nums = [int(s) for s in input]
print(nums[0], nums[-1])

class Node(object):
	def __init__(self, ch, md):
		self.children = ch
		self.metadata = md
	
	def value(self):
		if len(self.children) == 0:
			return sum(self.metadata)
		total = 0
		for m in self.metadata:
			if m > 0 and m <= len(self.children):
				total += self.children[m-1].value()
		return total

n = Node([1], [2])
print(n.children)

total = 0

def read_node(data):
	global total
	nc, nm, rest = data[0], data[1], data[2:]
	chs = []
	md = []
	for i in range(nc):
		ch, rest = read_node(rest)
		chs.append(ch)
	for i in range(nm):
		md.append(rest[i])
		total += rest[i]
	rest = rest[nm:]
	return Node(chs, md), rest
	
n, _ = read_node(nums)
print(total)
print(n.value())
