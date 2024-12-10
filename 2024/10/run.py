from me import *

input = get_data_2024(10)

input = input_test

Point = namedtuple("Point", "x y")
Cell = namedtuple("Cell", "point value")

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
		# unchecked! will fail on edges, so only use
		# with a padded grid where you won't hit the edges
		i,j = cell.point
		return [self.cells[jj][ii] for (ii,jj) in [
			(i,j-1),
			(i-1,j),
			(i+1,j),
			(i,j+1),
		]]

def rep_grid(g):
    return "\n".join("".join(row) for row in g)

def padded(N, c, grid):
	gx = len(grid[0])
	return (
		[[c] * (gx+2*N)] * N
		+ [[c]*N + row + [c]*N for row in grid]
		+ [[c] * (gx+2*N)] * N
	)

grid_data = lmap(partial(lmap, int), input.strip().split("\n"))
grid_data = padded(1, -1, grid_data)
g = Grid(grid_data)
starts = [c for c in g if c.value == 0]

# Part 1

def reachable(g, c):
	if c.value == 9:
		return set([c.point])
	return set.union(set(), *[reachable(g, n) for n in g.nabes(c) if n.value == c.value+1])


result1 = sum(len(reachable(g, s)) for s in starts)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=10)

# Part 2

def rating(g, c):
	if c.value == 9:
		return 1
	return sum(rating(g, n) for n in g.nabes(c) if n.value == c.value+1)


result2 = sum(rating(g, s) for s in starts)

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=10)
