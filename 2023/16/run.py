from me import *

input = get_data_2023(16)

input = input_test

D = (0,1)
U = (0,-1)
L = (-1,0)
R = (1,0)

# Part A

g = lmap(list, input.splitlines())

def rep_grid(g):
	return "\n".join("".join(row) for row in g)

#print(rep_grid(g))

visited = set()
to_visit = [((0,0), R)]
while to_visit:
	nxt = to_visit.pop()
	if nxt in visited:
		continue
	(i,j), dir = nxt
	if i < 0 or i >= len(g[0]) or j < 0 or j >= len(g):
		continue
	visited.add(nxt)

	cur = g[j][i]
	if cur == "." or (cur == "|" and dir in [U,D]) or (cur == "-" and dir in [L,R]):
		to_visit.append(((i + dir[0], j + dir[1]), dir))
	elif cur == "|":
		to_visit.append(((i,j-1), U))
		to_visit.append(((i,j+1), D))
	elif cur == "-":
		to_visit.append(((i-1,j), L))
		to_visit.append(((i+1,j), R))
	elif cur in "/\\":
		nxtdir = {
			"/": {L:D, R:U, D:L, U:R},
			"\\": {L:U, R:D, D:R, U:L},
			}[cur][dir]
		to_visit.append(((i+nxtdir[0], j+nxtdir[1]), nxtdir))
	else:
		assert(false)
		
resultA = len(set(v[0] for v in visited))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=16)

# Part B

import sys
sys.setrecursionlimit(10000)

# map of (pos,dir) => set(pos)
known_energized = {}

# returns a set of energized points, and a set of points we stopped at because they were in visited.
# if the second set is non-empty the result is incomplete until we've bubbled back to those points
def energized(start, visited):
	if start in known_energized:
		return known_energized[start], set()
	if start in visited:
		return set(), set([start])
	(i,j), dir = start
	if i < 0 or i >= len(g[0]) or j < 0 or j >= len(g):
		return set(), set()
	visited = visited.union({start})

	to_visit = []
	cur = g[j][i]
	if cur == "." or (cur == "|" and dir in [U,D]) or (cur == "-" and dir in [L,R]):
		to_visit.append(((i + dir[0], j + dir[1]), dir))
	elif cur == "|":
		to_visit.append(((i,j-1), U))
		to_visit.append(((i,j+1), D))
	elif cur == "-":
		to_visit.append(((i-1,j), L))
		to_visit.append(((i+1,j), R))
	elif cur in "/\\":
		nxtdir = {
			"/": {L:D, R:U, D:L, U:R},
			"\\": {L:U, R:D, D:R, U:L},
			}[cur][dir]
		to_visit.append(((i+nxtdir[0], j+nxtdir[1]), nxtdir))
	else:
		assert(false)
	
	subs = [energized(nxt, visited) for nxt in to_visit]
	
	res = set([start])
	loops = set()
	for sub, loopbacks in subs:
		res.update(sub)
		loops.update(loopbacks)
	loops.difference_update({start})
	if not loops:
		known_energized[start] = res
	return res, loops

# compute downstream sets from all edges
starts = (
	[((0,j), R) for j in range(len(g))]
	+ [((len(g[0])-1,j), L) for j in range(len(g))]
	+ [((i,0), D) for i in range(len(g[0]))]
	+ [((i,len(g)-1), U) for i in range(len(g[0]))]
)
resultB = 0
for s in starts:
	res, _ = energized(s, set())
	resultB = max(resultB, len(set(s[0] for s in res)))
	

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=16)
