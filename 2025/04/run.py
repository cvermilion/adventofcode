from me import *

DAY=4

input = get_data_2025(DAY)

input = input_test

PointT = namedtuple("Point", "x y")
class Point(PointT):
	pass
	
class Cell(object):
	def __init__(self, point, value):
		self.point = point
		self.value = value
	
	def __str__(self):
		return "{}@({},{})".format(self.value, self.point.x, self.point.y)
	
class Grid(object):
	def __init__(self, grid):
		self.cells = [[Cell(Point(i,j), val) for (i,val) in enumerate(row)] for (j,row) in enumerate(grid)]
	
	def __iter__(self):
		for row in self.cells:
			for c in row:
				yield c
	
	def __str__(self):
		return "\n".join("".join(str(c.value) for c in row) for row in self.cells)
	
	def nabes(self, cell):
		# unchecked, don't fall off the map
		i,j = cell.point
		return [self.cells[jj][ii] for (ii,jj) in [
			(i-1,j-1),
			(i,j-1),
			(i+1,j-1),
			(i-1,j),
			(i+1,j),
			(i-1,j+1),
			(i,j+1),
			(i+1,j+1),
		]]

def padded(N, c, grid):
	gx = len(grid[0])
	return (
		[[c] * (gx+2*N)] * N
		+ [[c]*N + row + [c]*N for row in grid]
		+ [[c] * (gx+2*N)] * N
	)

grid_data = lmap(list, input.splitlines())
grid_data = padded(1, ".", grid_data)
grid = Grid(grid_data)
#print(grid)
#print()

# Part 1

rolls = [c for c in grid if c.value == "@"]

result1 = count(r for r in rolls if count(n for n in grid.nabes(r) if n.value == "@") < 4)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=DAY)

# Part 2

removed = 0
to_remove = [r for r in rolls if count(n for n in grid.nabes(r) if n.value == "@") < 4]
while to_remove:
	removed += len(to_remove)
	for r in to_remove:
		r.value = "."
	rolls = [c for c in rolls if c.value == "@"]
	to_remove = [r for r in rolls if count(n for n in grid.nabes(r) if n.value == "@") < 4]
	
result2 = removed
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=DAY)
