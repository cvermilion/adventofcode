from me import *
from sickos.yes import *
from collections import namedtuple
from queue import PriorityQueue

input = get_data_2023(23)

#input = input_test

D = (0,1)
U = (0,-1)
L = (-1,0)
R = (1,0)

hill_dir = {"v": D, "^": U, "<": L, ">": R}

# Part A

g = lmap(list, input.splitlines())

start = (g[0].index("."), 0)
end = (g[-1].index("."), len(g)-1)

def rep_grid(g):
	return "\n".join("".join(map(str,row)) for row in g)

#print(rep_grid(g))

# path just for debugging
State = namedtuple("State", ["score", "pos", "visited", "path"])

nxt = (start[0], start[1]+1)
start_state = State(-1, nxt, {start, nxt}, [start, nxt])

best_sol = None
to_check = PriorityQueue()
to_check.put(start_state)

while not to_check.empty():
	cur = to_check.get()
	if cur.pos == end:
		if not best_sol or (-cur.score > best_sol):
			best_sol = -cur.score
		continue

	# compute next steps
	for dir in [R,L,U,D]:
		i,j = cur.pos[0]+dir[0], cur.pos[1]+dir[1]
		if (i,j) in cur.visited:
			continue
		score = -cur.score + 1
		new_visited = set([(i,j)])
		path = cur.path[:] + [(i,j)]
		match g[j][i]:
			case "#":
				continue
			case ".":
				pass
			case "<" | ">" | "v" | "^":
				if not hill_dir[g[j][i]] == dir:
					# can only go downhill
					continue
				score += 1
				i,j = i+dir[0], j+dir[1]
				if (i,j) in cur.visited:
					continue
				new_visited.add((i,j))
				path.append((i,j))
					
		to_check.put(State(-score, (i,j), set.union(cur.visited, new_visited), path))

resultA = best_sol

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=23)

# Part B

def next_node(node, cur):
	# returns the next node, the distance to it, and the other positions out of it
	steps = 1 # always start one step toward the next node
	visited = set([node, cur])
	while True:
		nxt = set()
		for dir in [R,L,U,D]:
			i,j = cur[0]+dir[0], cur[1]+dir[1]
			if (i,j) in visited or g[j][i] == "#":
				continue
			nxt.add((i,j))
		if len(nxt) == 1:
			cur = nxt.pop()
			steps += 1
			visited.add(cur)
			if cur == end:
				return cur, steps, set()
		else:
			return cur, steps, nxt
		
# compute node graph equivalent of maze
nodes = {start: set()}
to_check = [(start, nxt)]
while to_check:
	(prev_node, cur) = to_check.pop()
	node, steps, nxt = next_node(prev_node, cur)
	nodes[prev_node].add((steps, node))
	if not node in nodes:
		nodes[node] = set()
		# now add other paths out of node
		for n in nxt:
			to_check.append((node, n))
	nodes[node].add((steps, prev_node))

# now find longest path through the graph
start_state = State(0, start, {start}, [start])

to_check = PriorityQueue()
to_check.put(start_state)

best_sol = None

while not to_check.empty():
	cur = to_check.get()
	if cur.pos == end:
		if not best_sol or (-cur.score > best_sol):
			best_sol = -cur.score
		continue

	# compute next steps
	for (steps, nxt) in nodes[cur.pos]:
		if nxt not in cur.visited:
			to_check.put(State(cur.score - steps, nxt, set.union(cur.visited, {nxt}), cur.path + [nxt]))

resultB = best_sol

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=23)
