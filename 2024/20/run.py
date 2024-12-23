from me import *
from queue import PriorityQueue

input = get_data_2024(20)
min_improvement = 100

input = input_test
min_improvement = 1

PointT = namedtuple("Point", "x y")
VecT = namedtuple("Vec", "x y")

class Vec(VecT):
	def mag(self):
		return abs(self.x) + abs(self.y)
	
	def __add__(self, v2):
		return Vec(self.x+v2.x, self.y+v2.y)
		
	def __mul__(self, a):
		return Vec(a*self.x, a*self.y)
	
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

start, end = grid.find("S"), grid.find("E")
best = best_cost(start, end)

# Mark the outer walls a separate value, we don't cheat through here
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

best_no_cheating, best_to_no_cheating = find_sol()

# Enumerate all start and end points of a cheat run, then:
# find cost(start, start_cheat) for all sc
# find cost(end_cheat, end) for all ec
# for all (sc, ec) pairs check if cost(sc,ec) < 20 and if total cost is low enough

def find_cost_to_starts(max_cost):
	State = namedtuple("State", ["score", "pos"])
	start_state = State(0, start)
	
	to_check = PriorityQueue()
	to_check.put(start_state)
	while not to_check.empty():
		cur = to_check.get()
		
		if cur.score > max_cost:
			break
		
		if cur.pos.start_cost is not None and cur.score >= cur.pos.start_cost:
			continue
		cur.pos.start_cost = cur.score
	
		for nabe in grid.nabes(cur.pos):
			if nabe.value not in "#X":
				to_check.put(State(cur.score+1, nabe))

def find_cost_to_ends(max_cost):
	State = namedtuple("State", ["score", "pos"])
	start_state = State(0, end)
	
	to_check = PriorityQueue()
	to_check.put(start_state)
	while not to_check.empty():
		cur = to_check.get()
		
		if cur.score > max_cost:
			break
		
		if cur.pos.end_cost is not None and cur.score >= cur.pos.end_cost:
			continue
		cur.pos.end_cost = cur.score
	
		for nabe in grid.nabes(cur.pos):
			if nabe.value not in "#X":
				to_check.put(State(cur.score+1, nabe))

find_cost_to_starts(best_no_cheating)
find_cost_to_ends(best_no_cheating)

scs = [c for c in grid if c.value in ".S" and c.start_cost is not None]
ecs = [c for c in grid if c.value in ".E" and c.end_cost is not None]

def num_cheats(max_cheat, min_improvement):
	max_cost = best_no_cheating - min_improvement
	tot = 0
	for sc in scs:
		for ec in ecs:
			if ec == sc:
				continue
			non_cheat = sc.start_cost + ec.end_cost
			if non_cheat <= max_cost:
				cheat = (ec.point-sc.point).mag()
				if cheat is not None and cheat <= max_cheat and non_cheat + cheat <= max_cost:
					tot += 1
	return tot

# Part 1

result1 = num_cheats(2, min_improvement)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=20)

result2 = num_cheats(20, min_improvement)

print("Part 2:", result2) 
#aocd.submit(result2, part="b", day=20)

