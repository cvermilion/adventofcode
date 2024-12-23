from me import *
from queue import PriorityQueue
import json

input = get_data_2024(20)

#input = input_test

PointT = namedtuple("Point", "x y")
VecT = namedtuple("Vec", "x y")

class Vec(VecT):
	def mag(self):
		return abs(self.x) + abs(self.y)
	
	def __add__(self, v2):
		return Vec(self.x+v2.x, self.y+v2.y)
		
	def __mul__(self, a):
		return Vec(a*self.x, a*self.y)
	
	def decompose(self):
		parts = []
		if self.x > 0:
			parts.append((E, self.x))
		elif self.x < 0:
			parts.append((W, -self.x))
		if self.y > 0:
			parts.append((S, self.y))
		elif self.y < 0:
			parts.append((N, -self.y))
		return parts

class Point(PointT):
	def __sub__(self, x):
		if isinstance(x, Point):
			p2 = x
			return Vec(self.x-p2.x, self.y-p2.y)
		else:
			# assume Vec
			v = x
			return Point(self.x-v.x, self.y-v.y)
	
	def __add__(self, vec):
		return Point(self.x + vec.x, self.y +vec.y)
	
class Cell(object):
	def __init__(self, point, value):
		self.point = point
		self.value = value
		self.start_cost = None
		self.end_cost = None
	
	def __str__(self):
		return "{}@({},{})".format(self.value, self.point.x, self.point.y)
	
	def __lt__(self, c):
		return self.point < c.point and (self.value is None or self.value < c.value)

class Grid(object):
	def __init__(self, grid):
		self.cells = [[Cell(Point(i,j), val) for (i,val) in enumerate(row)] for (j,row) in enumerate(grid)]
	
	def __iter__(self):
		for row in self.cells:
			for c in row:
				yield c
	
	def __str__(self):
		return "\n".join("".join(str(c.value) for c in row) for row in self.cells)
	
	def find(self, val):
		for c in self:
			if c.value == val:
				return c
		return None
		
	def step(self, c, dir):
		x,y = c.point.x, c.point.y
		return self.cells[y+dir.y][x+dir.x]
	
	def nabes(self, cell):
		# unchecked, dont fall off the map
		i,j = cell.point
		return [self.cells[jj][ii] for (ii,jj) in [
			(i,j-1),
			(i-1,j),
			(i+1,j),
			(i,j+1),
		]]

def best_cost(c1, c2):
	return (c2.point-c1.point).mag()

State = namedtuple("State", ["best", "score", "pos"])

grid_data = lmap(list, input.splitlines())
grid = Grid(grid_data)
#print(grid)
#print()
start, end = grid.find("S"), grid.find("E")
best = best_cost(start, end)

for c in grid:
	x,y = c.point
	if x in (0, len(grid.cells[0])-1) or y in (0, len(grid.cells)-1):
		c.value = "X"

def find_sol():
	start_state = State(best, 0, start)
	
	# map of pos => score
	best_to = {}
	best_sol = None
	
	to_check = PriorityQueue()
	to_check.put(start_state)
	
	while not to_check.empty():
		cur = to_check.get()
		if cur.pos == end:
			if not best_sol or (cur.score < best_sol):
				best_sol = cur.score
				best_to[end] = best_sol
			continue
		if best_sol and cur.best >= best_sol:
			# no better solutions possible
			break
		best_so_far = best_to.get(cur.pos)
		if best_so_far and cur.score >= best_so_far:
			continue
		best_to[cur.pos] = cur.score
	
		# compute next steps
		
		for nabe in grid.nabes(cur.pos):
			if nabe.value not in "#X":
				to_check.put(State(best_cost(nabe, end), cur.score+1, nabe))
				
	return best_sol, best_to

State2 = namedtuple("State2", ["best", "score", "pos", "cheats"])

def find_sols(best_to_no_cheating, min_improvement):
	start_state = State2(best, 0, start, tuple())
	
	# map of {pos => {cheats => score}}
	best_to = {}
	max_best = best_to_no_cheating[end]-min_improvement
	print("max best:", max_best)
	
	to_check = PriorityQueue()
	to_check.put(start_state)
	
	while not to_check.empty():
		cur = to_check.get()
		curpt = cur.pos.point
		
		if cur.best > max_best:
			# no better solutions possible
			break
		
		if cur.cheats and cur.pos in best_to_no_cheating and cur.score > best_to_no_cheating[cur.pos] - min_improvement:
			#print("eorked")
			continue
		
		# update "best score to this point"
		if curpt not in best_to:
			best_to[curpt] = {cur.cheats: cur.score}
		else:
			best_to_here = best_to[curpt]
			s = best_to_here.get(cur.cheats)
			if s and s <= cur.score:
				# found a better way here, continue
				continue
			else:
				best_to_here[cur.cheats] = cur.score
		
		if cur.pos == end:
			continue
	
		# compute next steps
		
		for nabe in grid.nabes(cur.pos):
			if nabe.value == "X":
				# ignore outer walls
				continue
			nxt_score = cur.score+1
			best_rem = best_cost(nabe, end)+nxt_score
			nxt_pt = nabe.point
			if nabe.value != "#":
				cheats = cur.cheats if cur.cheats != (curpt,) else (curpt, nabe.point)
				to_check.put(State2(best_rem, nxt_score, nabe, cheats))
			elif len(cur.cheats) == 0:
				to_check.put(State2(best_rem, nxt_score, nabe, (nxt_pt,)))
				
	return best_to[end.point]

# Part 1


best_no_cheating, best_to_no_cheating = find_sol()
print("best is", best_no_cheating)
"""
with_cheating = find_sols(best_to_no_cheating, 100)
#print(with_cheating)

result1 = len(with_cheating)
print("Part 1:", result1)
#aocd.submit(result1, part="a", day=20)
"""

# Part 2

# Better alg: enumerate all start and end points of a cheat run, then:
# find cost(start, start_cheat) for all sc
# find cost(end_cheat, end) for all ec
# for all (sc, ec) pairs check if cost(sc,ec) < 20 and if total cost is low enough

def find_cost_to_starts(max_cost):
	# only sets c.cost for cells as close as max_cost
	State = namedtuple("State", ["score", "pos"])
	start_state = State(0, start)
	
	# map of pos => score
	best_to = {}
	
	to_check = PriorityQueue()
	to_check.put(start_state)
	
	while not to_check.empty():
		cur = to_check.get()
		curpt = cur.pos.point
		
		if cur.score > max_cost:
			break
		
		best_so_far = best_to.get(curpt)
		if best_so_far is not None and cur.score >= best_so_far:
			continue
		best_to[curpt] = cur.score
		
		cur.pos.start_cost = cur.score
	
		# compute next steps
		
		for nabe in grid.nabes(cur.pos):
			if nabe.value not in "#X":
				to_check.put(State(cur.score+1, nabe))

def find_cost_to_ends(max_cost):
	# only sets c.cost for cells as close as max_cost
	State = namedtuple("State", ["score", "pos"])
	start_state = State(0, end)
	
	# map of pos => score
	best_to = {}
	
	to_check = PriorityQueue()
	to_check.put(start_state)
	
	while not to_check.empty():
		cur = to_check.get()
		curpt = cur.pos.point
		
		best_so_far = best_to.get(curpt)
		if best_so_far is not None and cur.score >= best_so_far:
			continue
		best_to[curpt] = cur.score
		
		cur.pos.end_cost = cur.score
	
		# compute next steps
		
		for nabe in grid.nabes(cur.pos):
			if nabe.value not in "#X":
				to_check.put(State(cur.score+1, nabe))

def find_cheat_cost(start, end, max_cost):
	# return None if no path or longer than max
	State = namedtuple("State", ["score", "pos"])
	start_state = State(0, start)
	
	# map of pos => score
	best_to = {}
	
	to_check = PriorityQueue()
	to_check.put(start_state)
	
	while not to_check.empty():
		cur = to_check.get()
		curpt = cur.pos.point
		
		if cur.score > max_cost:
			return None
		
		best_so_far = best_to.get(curpt)
		if best_so_far is not None and cur.score >= best_so_far:
			continue
		best_to[curpt] = cur.score
	
		# compute next steps
		
		for nabe in grid.nabes(cur.pos):
			if nabe.value == "#":
				to_check.put(State(cur.score+1, nabe))
			elif nabe == end:
				return cur.score+1
					
find_cost_to_starts(best_no_cheating)
find_cost_to_ends(best_no_cheating)

scs = [c for c in grid if c.value in ".S" and c.start_cost is not None]
ecs = [c for c in grid if c.value in ".E" and c.end_cost is not None]

max_cost = best_no_cheating - 100
tot = 0
for sc in scs:
	for ec in ecs:
		if ec == sc:
			continue
		non_cheat = sc.start_cost + ec.end_cost
		if non_cheat <= max_cost:
			cheat = (ec.point-sc.point).mag()
			#cheat = find_cheat_cost(sc, ec, max_cost-non_cheat)
			# 2 for part 1
			if cheat is not None and cheat <= 100 and non_cheat + cheat <= max_cost:
				#print(str(sc), str(ec))
				tot += 1

result2 = tot

print("Part 2:", result2) 
#aocd.submit(result2, part="b", day=20)

