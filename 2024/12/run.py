from me import *

input = get_data_2024(12)

input = input_test

#input = open("input_test1.txt").read().strip()
#input = open("input_test2.txt").read().strip()
#input = open("input_test3.txt").read().strip()
#input = open("input_test4.txt").read().strip()

Point = namedtuple("Point", "x y")
Cell = namedtuple("Cell", "point value")

class Garden:
	def __init__(self, cell):
		self.cells = set([cell])
		self.name = cell.value
		self.perimeter = 0
		self.boundaries = set()
	def __repr__(self):
		return repr((self.name,self.perimeter,self.cells,self.boundaries))

class Grid(object):
	def __init__(self, grid):
		self.cells = [[Cell(Point(i,j), val) for (i,val) in enumerate(row)] for (j,row) in enumerate(grid)]
	
	def __iter__(self):
		for row in self.cells:
			for c in row:
				yield c
	
	def __str__(self):
		return "\n".join("".join(str(c.value) for c in row) for row in self.cells)
	
	def contains(self, pt):
		return pt.x >= 0 and pt.x < len(self.cells[0]) and pt.y >= 0 and pt.y < len(self.cells)
	
	def nabes(self, cell):
		# unchecked, don't fall off the map
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

grid_data = lmap(list, input.splitlines())
# pad twice because in part 2 we check neighbors of neighbors
grid_data = padded(2, None, grid_data)

grid = Grid(grid_data)
#print(grid)

# Part 1

to_check = set([grid.cells[2][2]])
visited = set()
gardens = []

while to_check:
	c = to_check.pop()
	if c in visited:
		continue
	g = Garden(c)
	gardens.append(g)
	
	to_check_g = set([c])
	while to_check_g:
		c = to_check_g.pop()
		visited.add(c)
		g.cells.add(c)
		for n in grid.nabes(c):
			if n.value != c.value:
				g.perimeter += 1
				g.boundaries.add((c,n))
			if n.value and n not in visited:
				if n.value != c.value:
					to_check.add(n)
				else:
					to_check_g.add(n)

result1 = sum(len(g.cells)*g.perimeter for g in gardens)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=12)

# Part 2

# A boundary is a two-tuple of cells, the first one is inside and the second is outside
# Two boundaries are adjacent if their insides are neighbors and their outsides are neighbors.
def adjacent(b1, b2):
	return b1[0] in grid.nabes(b2[0]) and b1[1] in grid.nabes(b2[1])

def sides(boundaries):
	# Form groups by clustering adjacent boundaries, the number of sides is the number of groups.
	groups = 0
	remaining = set(list(boundaries))
	while remaining:
		cur = set([remaining.pop()])
		to_check = set(list(cur))
		while to_check:
			matching = set(b for b in remaining if any(adjacent(b, b2) for b2 in to_check))
			cur.update(matching)
			remaining.difference_update(matching)
			to_check = matching
		groups += 1
	return groups

result2 = sum(len(g.cells)*sides(g.boundaries) for g in gardens)

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=12)
