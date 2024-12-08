from me import *
from math import gcd

input = get_data_2024(8)

#input = input_test

class Point(tuple):
	def __new__(cls,x,y):
		self = super().__new__(cls,[x,y])
		return self

PointT = namedtuple("Point", "x y")
VecT = namedtuple("Vec", "x y")

class Vec(VecT):
	def mag(self):
		return abs(self.x) + abs(self.y)
	
	def unit(self):
		# the shortest vector v such that self==a*v for positive integer a
		a = gcd(self.x, self.y)
		return Vec(int(self.x/a), int(self.y/a))
	
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
	
	def contains(self, pt):
		return pt.x >= 0 and pt.x < len(self.cells[0]) and pt.y >= 0 and pt.y < len(self.cells)

# Part 1

grid = lmap(list, input.strip().split("\n"))

def rep_grid(g):
    return "\n".join("".join(row) for row in g)

Ni = len(grid[0])
Nj = len(grid)

#print(rep_grid(grid))

g = Grid(grid)

anntennae = {}
for (pt,val) in g:
	if val == ".":
		continue
	if val not in anntennae:
		anntennae[val] = set([pt])
	else:
		anntennae[val].add(pt)

def antinodes(a1, a2):
	delta = a2-a1
	n1 = a2 + delta
	n2 = a1 - delta
	return set([n1,n2])

all_antis = set()
for freq, ants in anntennae.items():
	for a1 in ants:
		for a2 in ants:
			if a1==a2:
				continue
			all_antis.update(antinodes(a1,a2))

result1 = sum(1 for p in all_antis if g.contains(p))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=8)

# Part 2

def antinodes(a1, a2):
	# choose a2 as rightmost
	if a1.x > a2.x:
		a1,a2 = a2,a1
	
	delta = a2-a1
	step = delta.unit()
	max_left = int(a1.x / step.x)
	max_right = int((Ni-1-a1.x) / step.x)
	return set(a1 - (step*n) for n in range(max_left+1)).union(set(a1 + (step*n) for n in range(max_right+1)))

all_antis = set()
for freq, ants in anntennae.items():
	for a1 in ants:
		for a2 in ants:
			if a1==a2:
				continue
			all_antis.update(antinodes(a1,a2))

result2 = sum(1 for p in all_antis if g.contains(p))

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=8)
