input_test = """1
2
-3
3
-2
0
4"""

input = input_test
input = open("input.py").read()

class Node (object):
	def __init__(self, n):
		self.n = n
		self.nxt = None
		self.prev = None

def init_nodes(key):
	nodes = [Node(n*key) for n in map(int, input.splitlines())]
	zero = None
	for i,n in enumerate(nodes):
		if n.n == 0:
			zero = n
		nodes[i-1].nxt = n
		n.prev = nodes[i-1]
	return nodes, zero

def advance(nodes, node, steps):
	if steps == 0:
		return
	prev = node.prev
	nxt = node.nxt
	node.nxt.prev = prev
	prev.nxt = nxt
	
	if steps > 0:
		for i in range(steps % (len(nodes)-1)):
			prev = nxt
			nxt = nxt.nxt
	else:
		for i in range((-steps) % (len(nodes)-1)):
			nxt = prev
			prev = prev.prev
			
	node.nxt = nxt
	node.prev = prev
	prev.nxt = node
	node.nxt.prev = node

def print_chain(first):
	s = "{} -> ".format(first.n)
	nxt = first.nxt
	while nxt is not first:
		s += "{} -> ".format(nxt.n)
		nxt = nxt.nxt
	print(s)

def print_chain_rev(first):
	s = "{} <- ".format(first.n)
	prev = first.prev
	while prev is not first:
		s += "{} <- ".format(prev.n)
		prev = prev.prev
	print(s)

def run(times):
	for i in range(times):
		for n in nodes:
			advance(nodes, n, n.n)

def result(zero):
	# make an array starting at zero:
	a = [zero]
	nxt = zero.nxt
	while nxt is not zero:
		a.append(nxt)
		nxt = nxt.nxt
	
	return sum(a[x % len(a)].n for x in [1000, 2000, 3000])

nodes, zero = init_nodes(1)
run(1)
print(result(zero))

# part 2

key = 811589153
nodes, zero = init_nodes(key)
run(10)
print(result(zero))
