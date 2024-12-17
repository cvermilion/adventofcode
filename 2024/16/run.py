from me import *
from queue import PriorityQueue

input = get_data_2024(16)

input = input_test
#input = open("input_test1.txt").read().strip()

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
	
	def __str__(self):
		return "{}@({},{})".format(self.value, self.point.x, self.point.y)
	
	def __lt__(self, c):
		return self.point < c.point and self.value < c.value

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

grid_data = lmap(list, input.splitlines())

grid = Grid(grid_data)
#print(grid)
#print()

N,E,S,W = Vec(0,-1), Vec(1,0), Vec(0,1), Vec(-1,0)

start, end = grid.find("S"), grid.find("E")
start_dir = E

# Part 1

def best_cost(c1, c2, dir):
	moves = 0
	turns = 0
	for (d, m) in (c2.point-c1.point).decompose():
		moves += m
		if d == dir:
			continue
		elif d == dir*(-1):
			turns = 2
		elif turns == 0:
			turns = 1
	return 1000*turns + moves

State = namedtuple("State", ["best", "score", "pos", "dir"])
best = best_cost(start, end, start_dir)
start_state = State(best, 0, start, start_dir)

# map of (pos,dir) => score
best_to = {}
best_sol = None

to_check = PriorityQueue()
to_check.put(start_state)

while not to_check.empty():
	cur = to_check.get()
	if cur.pos == end:
		if not best_sol or (cur.score < best_sol):
			best_sol = cur.score
		continue
	if best_sol and cur.best >= best_sol:
		# no better solutions possible
		break
	best_so_far = best_to.get((cur.pos, cur.dir))
	if best_so_far and cur.score >= best_so_far:
		continue
	best_to[(cur.pos, cur.dir)] = cur.score

	# compute next steps
	# two possibilities: move or turn
	
	# move
	nxt_pos = grid.step(cur.pos, cur.dir)
	if nxt_pos.value != "#":
		new_best = cur.score+1+best_cost(nxt_pos, end, cur.dir)
		to_check.put(State(new_best, cur.score+1, nxt_pos, cur.dir))
	
	# turn
	left = {N:W,W:S,S:E,E:N}[cur.dir]
	right = {N:E,E:S,S:W,W:N}[cur.dir]
	for new_dir in [left,right]:
		new_best = cur.score+1000+best_cost(cur.pos, end, new_dir)
		to_check.put(State(new_best, cur.score+1000, cur.pos, new_dir))

result1 = best_sol

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=16)

# Part 2

State = namedtuple("State", ["best", "score", "pos", "dir", "visited"])
start_state = State(best, 0, start, start_dir, {start})

best_to = {}
to_check = PriorityQueue()
to_check.put(start_state)

while not to_check.empty():
	cur = to_check.get()
	if cur.best > best_sol:
		# no more best sols possible
		break
	if cur.pos == end:
		continue
	
	# compute next steps
	# two possibilities: move or turn
	
	next_states = []
	# move
	nxt_pos = grid.step(cur.pos, cur.dir)
	if nxt_pos.value != "#":
		new_best = cur.score+1+best_cost(nxt_pos, end, cur.dir)
		next_states.append(State(new_best, cur.score+1, nxt_pos, cur.dir, cur.visited.union({nxt_pos})))
	
	# turn
	left = {N:W,W:S,S:E,E:N}[cur.dir]
	right = {N:E,E:S,S:W,W:N}[cur.dir]
	for new_dir in [left,right]:
		new_best = cur.score+1000+best_cost(cur.pos, end, new_dir)
		next_states.append(State(new_best, cur.score+1000, cur.pos, new_dir, cur.visited))
	
	for st in next_states:
		key = (st.pos, st.dir)
		if key not in best_to:
			best_to[key] = (st.score, st.visited)
			to_check.put(st)
		else:
			(score, all_visited) = best_to[key]
			if st.score < score:
				best_to[key] = (st.score, st.visited)
				to_check.put(st)
			elif st.score == score:
				all_visited.update(st.visited)

all_best = set.union(*[best_to.get((end,d), (0, set()))[1] for d in [N,S,E,W]])
result2 = len(all_best)

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=16)
