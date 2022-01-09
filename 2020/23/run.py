from collections import deque

data = "389125467"
data = "598162734"
state = deque(map(int, data))

def step(state):
	cur = state[0]
	# move current to back
	state.rotate(-1)
	# grab next three
	movers = state.popleft(), state.popleft(), state.popleft()
	# lower cur (wrapping in 1-9), skipping numbers in the set of three we picked out
	dest = (cur - 1 + 8) % 9 + 1
	while dest in movers:
		dest = (dest - 1 + 8) % 9 + 1
	# insert movers after dest
	idx = state.index(dest)
	for i, x in enumerate(movers):
		state.insert(idx+i+1, x)
	# new cur is in front

for i in range(100):
	step(state)

state.rotate(-state.index(1))
state.popleft()
print("Part 1:", "".join(map(str, state)))

# Part 2

class Cup(object):
	def __init__(self, val):
		self.value = val
		self.next = None
		
state = list(map(Cup, list(map(int, data)) + list(range(10, 1000001))))
lookup = {}
for i, c in enumerate(state):
	state[i-1].next = c
	lookup[c.value] = c

cur = state[0]

def step2():
	# grab next three
	global cur
	movers = cur.next, cur.next.next, cur.next.next.next
	# lower cur (wrapping in 1-1e6), skipping numbers in the set of three we picked out
	dest = (cur.value + (1000000 - 2)) % 1e6 + 1
	while dest in [m.value for m in movers]:
		dest = (dest + (1000000 - 2)) % 1e6 + 1
	# insert movers after dest
	dest_cup = lookup[dest]
	after_dest = dest_cup.next
	dest_cup.next = movers[0]
	cur.next = movers[2].next
	movers[2].next = after_dest
	cur = cur.next
	

for i in range(10000000):
	if i % 100000 == 0:
		print(i/100000, "/", 100)
	step2()

one = lookup[1]
result = one.next.value * one.next.next.value
print("Part 2:", result)
