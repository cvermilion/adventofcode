from me import *

input = get_data_2024(6)

#input = input_test

N,E,S,W = (0,-1), (1,0), (0,1), (-1,0)

Path = namedtuple("Path", "dir mag")

PointT = namedtuple("Point", "x y")
class Point(PointT):
	def __sub__(self, p2):
		# None if not in the same row or column
		if self.x == p2.x:
			if self.y > p2.y:
				return Path(S, self.y-p2.y)
			else:
				return Path(N, p2.y-self.y)
		elif self.y == p2.y:
			if self.x > p2.x:
				return Path(E, self.x-p2.x)
			else:
				return Path(W, p2.x-self.x)
		return None
	
	def __add__(self, path):
		return Point(self.x + path.dir.x*path.mag, self.y + path.dir.y*path.mag)

Cell = namedtuple("Cell", "point value")

class Grid(object):
	def __init__(self, grid):
		Ni = len(grid[0])
		Nj = len(grid)
		self.cells = [[Cell(Point(i,j), val) for (i,val) in enumerate(row)] for (j,row) in enumerate(grid)]
	
	def __iter__(self):
		for row in self.cells:
			for c in row:
				yield c

# Part 1

grid = lmap(list, input.strip().split("\n"))

Ni = len(grid[0])
Nj = len(grid)

g = Grid(grid)

start, start_dir = None, None
obstacles = set()
boundary = set()
for c in g:
	if c.value in "<>^v":
		start = c.point
		start_dir = {"v": S, "^": N, ">": E, "<": W}[c.value]
	if c.value == "#":
		obstacles.add(c.point)
	if c.value == "0":
		boundary.add(c.point)

visited = set([start])
cur, dir = start, start_dir
while True:
	closest = None
	for obs in obstacles:
		path = obs-cur
		if not path or path.dir != dir:
			continue
		if not closest or path.mag < closest.mag:
			closest = path
	
	if closest:
		# go one short of the obstacle and turn
		next = cur + Path(closest.dir, closest.mag-1)
		visited.update(set(cur + Path(closest.dir, m) for m in range(1, closest.mag)))
		cur = next
		dir = {N:E,E:S,S:W,W:N}[dir]
	else:
		# hit a boundary
		if dir == E:
			visited.update(set(Point(i, cur.y) for i in range(cur.x+1, Ni)))
		elif dir == S:
			visited.update(set(Point(cur.x, j) for j in range(cur.y+1, Nj)))
		elif dir == W:
			visited.update(set(Point(i, cur.y) for i in range(cur.x)))
		elif dir == N:
			visited.update(set(Point(cur.x, j) for j in range(cur.y)))
		break

result1 = len(visited)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=6)

# Part 2

def has_loop(obstacle):
	cur, dir = start, start_dir
	visited = set([(start, start_dir)])
	new_obstacles = obstacles.union(set([obstacle]))
	while True:
		closest = None
		for obs in new_obstacles:
			path = obs-cur
			if not path or path.dir != dir:
				continue
			if not closest or path.mag < closest.mag:
				closest = path
		
		if closest:
			# go one short of the obstacle and turn
			next = cur + Path(closest.dir, closest.mag-1)
			cur = next
			dir = {N:E,E:S,S:W,W:N}[dir]
			if (cur, dir) in visited:
				return True
			visited.add((cur, dir))
		else:
			# escape
			return False 

to_check = visited
to_check.remove(start)

result2 = sum(1 for o in to_check if has_loop(o))
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=6)
