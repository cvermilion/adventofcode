from me import *
from queue import PriorityQueue
import json

input = get_data_2024(18)
N = 71
part1_steps = 1024

#input = input_test
#N = 7
#part1_steps = 12

bytes = json.loads("[[{}]]".format(input.strip().replace("\n", "],[")))

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

def padded(N, c, grid):
	gx = len(grid[0])
	return (
		[[c] * (gx+2*N)] * N
		+ [[c]*N + row + [c]*N for row in grid]
		+ [[c] * (gx+2*N)] * N
	)

def best_cost(c1, c2):
	return (c2.point-c1.point).mag()

State = namedtuple("State", ["best", "score", "pos", "path"])

def find_sol(t):
	grid_data = [[None]*N for j in range(N)]
	for (i, (x,y)) in enumerate(bytes):
		if i < t:
			grid_data[y][x] = i+1
	grid_data = padded(1, 0, grid_data)
		
	grid = Grid(grid_data)
	start, end = grid.cells[1][1], grid.cells[N][N]
	best = best_cost(start, end)
	
	start_state = State(best, 0, start, {start.point})
	
	# map of pos => score
	best_to = {}
	best_sol = None
	best_path = None
	
	to_check = PriorityQueue()
	to_check.put(start_state)
	
	while not to_check.empty():
		cur = to_check.get()
		if cur.pos == end:
			if not best_sol or (cur.score < best_sol):
				best_sol = cur.score
				best_path = cur.path
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
			if nabe.value is None:
				to_check.put(State(best_cost(nabe, end), cur.score+1, nabe, cur.path.union({nabe.point})))
				
	return best_sol, best_path

# Part 1

result1 = find_sol(part1_steps)[0]
print("Part 1:", result1)
#aocd.submit(result1, part="a", day=18)

# Part 2

t = part1_steps
result2 = None
while t < len(bytes):
	sol, path = find_sol(t)
	if sol is None:
		result2 = "{},{}".format(*bytes[t-1])
		break
	t += 1
	# next byte that blocks the existing path
	while not Point(bytes[t-1][0]+1, bytes[t-1][1]+1) in path:
		t += 1

print("Part 2:", result2) 
#aocd.submit(result2, part="b", day=18)
