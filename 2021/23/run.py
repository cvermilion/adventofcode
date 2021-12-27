"""
top row: 0-10
wells at 2,4,6,8; depth 1-4 (1-2 for part 1)
"""

bottom = 2

# outer list (j) is horizontal, inner (i) is vertical
init_state = (
	(None,),
	(None,),
	(None, "A", "C"),
	(None,),
	(None, "D", "C"),
	(None,),
	(None, "A", "D"),
	(None,),
	(None, "B", "B"),
	(None,),
	(None,),
	)

def add(state, ii, jj, val):
	return tuple(tuple(state[j][i] if (i != ii or j != jj) else val for i in range(len(state[j]))) for j in range(11))

def col(c):
	return {"A": 2, "B": 4, "C": 6, "D": 8}[c]

def weight(c):
	return {"A": 1, "B": 10, "C": 100, "D": 1000}[c]
	
def min_cost(state):
	moved = {"A": 0, "B": 0, "C": 0, "D": 0}
	total = 0
	for j in range(11):
		for (i,c) in enumerate(state[j]):
			if not c or j == col(c):
				continue
			steps = i + abs(j - col(c)) + (moved[c]+1)
			moved[c] += 1
			total += steps * weight(c)
	return total
		
def nxt(state, cost):
	open = [c for c in "ABCD" if all(state[col(c)][i] in [c, None] for i in range(2, bottom+1)) and not state[col(c)][1]]
	
	moves = []
	# moving out of wells
	for c in "ABCD":
		if c not in open:
			for i in range(1, bottom+1):
				j0, i0 = (col(c), i)
				x = state[j0][i0]
				if x:
					# something here, we can make it to any open top space in either direction until we hit something
					for dir in [reversed(range(0, j0)), range(j0+1, 11)]:
						for j in dir:
							if state[j][0]:
								break
							if j in [2,4,6,8]:
								continue
							move = add(state, i0, j0, None)
							move = add(move, 0, j, x)
							moves.append((move, cost+ weight(x)*(i + abs(j0-j))))
					break
	
	# Moving into wells
	for c in open:
		jc = col(c)
		# if first thing we hit in either direction is the right kind
		for dir in [reversed(range(0, jc)), range(jc+1, 11)]:
			for j in dir:
				if not state[j][0]:
					continue
				if j in [2,4,6,8]:
					continue
				if state[j][0] != c:
					break
				move = add(state, 0, j, None)
				# lowest open spot in well
				i = 1
				for ii in range(2, bottom+1):
					if not state[jc][ii]:
						i = ii
					else:
						break
				move = add(move, i, jc, c)
				moves.append((move, cost+ weight(c)*(i + abs(jc-j))))
				break
				
	return moves

def ch(c):
	return c if c else "."
	
def rep(state):
	return "\n".join("".join(ch(state[j][i]) if len(state[j]) > i else "X" for j in range(11)) for i in range(bottom+1))

def do_step(states):
	state, (best_possible, cost) = min(states.items(), key=lambda kv: kv[1])
	if best_possible == cost:
		return (True, cost, cost)
	more = nxt(state, cost)
	del states[state]
	for (st, c) in more:
		bp = c + min_cost(st)
		if st not in states or states[st][0] > bp:
			states[st] = (bp, c)
	return False, best_possible, cost

# Part 1

states = {init_state: (min_cost(init_state), 0)}
cost = 0
best = 0
for i in range(10000):
	if i > 0 and i % 1000 == 0:
		print("step", i, len(states), cost, best)
	succ, best, cost = do_step(states)
	if succ:
		print("Part 1:", cost)
		break
		
# Part 2, takes a few minutes to run on an iphone SE2

init_state = (
	(None,),
	(None,),
	(None, "A", "D", "D", "C"),
	(None,),
	(None, "D", "C", "B", "C"),
	(None,),
	(None, "A", "B", "A", "D"),
	(None,),
	(None, "B", "A", "C", "B"),
	(None,),
	(None,),
	)
bottom = 4

states = {init_state: (min_cost(init_state), 0)}
cost = 0
best = 0
for i in range(1000000):
	if i > 0 and i % 5000 == 0:
		print("step", i, len(states), cost, best)
	succ, best, cost = do_step(states)
	if succ:
		print("Part 2:", cost)
		break
