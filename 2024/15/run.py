from me import *

input = get_data_2024(15)

input = input_test
#input = open("input_test1.txt").read().strip()

Vec = namedtuple("Vec", "x y")

PointT = namedtuple("Point", "x y")
class Point(PointT):
	def __add__(self, vec):
		return Point(self.x + vec.x, self.y +vec.y)

class Cell(object):
	def __init__(self, point, value):
		self.point = point
		self.value = value
	
class Grid(object):
	def __init__(self, grid):
		self.cells = [[Cell(Point(i,j), val) for (i,val) in enumerate(row)] for (j,row) in enumerate(grid)]
	
	def __iter__(self):
		for row in self.cells:
			for c in row:
				yield c
	
	def __str__(self):
		return "\n".join("".join(str(c.value) for c in row) for row in self.cells)
		
	def step(self, c, dir):
		x,y = c.point + dir
		return self.cells[y][x]

grid_data, moves_data = input.split("\n\n")
grid_data = lmap(list, grid_data.splitlines())

grid = Grid(grid_data)
#print(grid)
#print()

N,E,S,W = Vec(0,-1), Vec(1,0), Vec(0,1), Vec(-1,0)
moves = [{"v": S, "^": N, ">": E, "<": W}[m] for m in moves_data.replace("\n", "")]

# Part 1

def can_push(g, c, dir):
	nxt = g.step(c, dir)
	while nxt.value == "O":
		nxt = g.step(nxt, dir)
	return nxt.value != "#"

def do_push(g, c, dir):
	c.value = "."
	nxt = g.step(c, dir)
	if nxt.value == ".":
		# move into empty space
		nxt.value = "@"
		return nxt
	else:
		# push a line of boxes; only need to put robot in for
		# first box, add a box to the end
		first = nxt
		end = nxt
		while end.value == "O":
			end = g.step(end, dir)
		end.value = "O"
		first.value = "@"
		return first

robot = [c for c in grid if c.value == "@"][0]
for m in moves:
	if can_push(grid, robot, m):
		robot = do_push(grid, robot, m)

#print(grid)
#print()

result1 = sum(c.point.x + 100*c.point.y for c in grid if c.value == "O")

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=15)

# Part 2

def double(x):
	return {"@": "@.", ".": "..", "#": "##", "O": "[]"}[x]

expanded = [list("".join([double(x) for x in row])) for row in grid_data]
grid = Grid(expanded)

#print(grid)
#print()

def can_push(g, c, dir):
	nxt = g.step(c, dir)
	if nxt.value == ".":
		return True
	if nxt.value == "#":
		return False
	if dir in [E,W]:
		return can_push(g, nxt, dir)
	other = g.step(nxt, {"[":E,"]":W}[nxt.value])
	return can_push(g, nxt, dir) and can_push(g, other, dir)

def do_push(g, c, dir):
	nxt = g.step(c, dir)
	if nxt.value in "[]":
		if dir in [N,S]:
			other = g.step(nxt, {"[":E,"]":W}[nxt.value])
			do_push(g, other, dir)
		do_push(g, nxt, dir)
	nxt.value = c.value
	c.value = "."
	return nxt

robot = [c for c in grid if c.value == "@"][0]
for m in moves:
	if can_push(grid, robot, m):
		robot = do_push(grid, robot, m)
		
result2 = sum(c.point.x + 100*c.point.y for c in grid if c.value == "[")
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=15)
