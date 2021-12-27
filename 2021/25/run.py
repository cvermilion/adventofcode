data = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

data = open("input.py").read()

from enum import Enum, auto

class Cell(Enum):
	EMPTY = auto()
	EAST = auto()
	SOUTH = auto()

def cell(c):
	return {
		".": Cell.EMPTY,
		"v": Cell.SOUTH,
		">": Cell.EAST,
	}[c]

def cell_rep(c):
	return {
		Cell.EMPTY: ".",
		Cell.EAST: ">",
		Cell.SOUTH: "v",
	}[c]

grid = [[cell(c) for c in line] for line in data.strip().split("\n")]
Nx = len(grid[0])
Ny = len(grid)

def grid_rep(g):
	return "\n".join("".join(cell_rep(c) for c in row) for row in g)

def nxt(g, i, j):
	cur = g[j][i]
	if cur == Cell.EAST:
		right = g[j][(i+1) % Nx]
		if right == Cell.EMPTY:
			up = g[j-1][i]
			if up == Cell.SOUTH:
				return Cell.SOUTH
			return Cell.EMPTY
		else:
			return Cell.EAST
	if cur == Cell.SOUTH:
		down = g[(j+1) % Ny][i]
		downleft = g[(j+1)% Ny][i-1]
		downright = g[(j+1)%Ny][(i+1)%Nx]
		if (down == Cell.EMPTY and downleft != Cell.EAST) or (down == Cell.EAST and downright == Cell.EMPTY):
			return Cell.EMPTY
		else:
			return Cell.SOUTH
	# empty: does an EAST move in, or a SOUTH, or nothing
	left = g[j][i-1]
	if left == Cell.EAST:
		return Cell.EAST
	up = g[j-1][i]
	if up == Cell.SOUTH:
		return Cell.SOUTH
	return Cell.EMPTY
		
def do_step(g):
	return [[nxt(g, i, j) for i in range(Nx)] for j in range(Ny)]

prev = grid
n = 0
while n < 1000:
	grid = do_step(prev)
	n += 1
	if grid == prev:
		break
	prev = grid

print("Part 1:", n)
