from me import *
from collections import namedtuple
from queue import PriorityQueue

input = get_data_2023(17)

input = input_test

D = (0,1)
U = (0,-1)
L = (-1,0)
R = (1,0)
bw = {R:L, L:R, U:D, D:U}

# Part A

g = lmap(partial(lmap, int), input.splitlines())

def rep_grid(g):
	return "\n".join("".join(map(str,row)) for row in g)

#print(rep_grid(g))

State = namedtuple("State", ["best", "score", "pos", "trend"])

best = len(g) + len(g[0])
start = State(best, 0, (0,0), (R,0))

def find_best(min_run, max_run):
	best_to = {}
	best_sol = None

	to_check = PriorityQueue()
	to_check.put(start)

	while not to_check.empty():
		cur = to_check.get()
		if cur.pos == (len(g[0])-1, len(g)-1):
			if not best_sol or (cur.score < best_sol):
				best_sol = cur.score
				continue
		if best_sol and cur.best > best_sol:
			break
		key = (cur.pos, cur.trend)
		if key in best_to and best_to[key] <= cur.score:
			# Already found a better way here
			continue
		best_to[key] = cur.score
		
		# compute next steps
		for dir in [R,L,U,D]:
			if bw[cur.trend[0]] == dir:
				continue
			if cur.trend[1] < min_run and cur.trend[0] != dir:
				continue
			if cur.trend[0] == dir:
				if cur.trend[1] == max_run:
					continue
				trend = (dir, cur.trend[1]+1)
			else:
				trend = (dir, 1)
			
			i,j = cur.pos[0]+dir[0], cur.pos[1]+dir[1]
			# grid bounds
			if i < 0 or i >= len(g[0]) or j < 0 or j >= len(g):
				continue
			score = cur.score + g[j][i]
			best = (len(g)-1-j) + (len(g[0])-1-i) + score
			to_check.put(State(best, score, (i,j), trend))
	return best_sol

resultA = find_best(0, 3)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=17)

# Part B

resultB = find_best(4, 10)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=17)
