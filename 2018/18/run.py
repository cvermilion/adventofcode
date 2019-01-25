input = open("input.txt").readlines()
grid = [[input[j][i] for j in range(len(input))] for i in range(len(input[0])-1)]

def show(g):
	print("\n".join("".join(g[i][j] for i in range(len(g))) for j in range(len(g[0]))))

#show(grid)

from copy import deepcopy
grid2 = deepcopy(grid)

def neighbors(grid, i, j):
	max = len(grid)-1
	nn = []
	if i > 0:
		nn.append((i-1,j))
		if j > 0:
			nn.append((i-1,j-1))
		if j < max:
			nn.append((i-1,j+1))
	if j > 0:
		nn.append((i,j-1))
	if j < max:
		nn.append((i,j+1))
	if i < max:
		nn.append((i+1,j))
		if j > 0:
			nn.append((i+1,j-1))
		if j < max:
			nn.append((i+1,j+1))
	return [grid[i][j] for (i,j) in nn]
	
def updatex(old, new):
	for i in range(len(old)):
		for j in range(len(old[i])):
			val = old[i][j]
			new_val = val
			nn = neighbors(old, i, j)
			if val == ".":
				if len([n for n in nn if n == "|"]) >= 3:
					new_val = "|"
			elif val == "#":
				if not [n for n in nn if n == "|"] or not [n for n in nn if n == "#"]:
					new_val = "."
			elif val == "|":
				if len([n for n in nn if n == "#"]) >= 3:
					new_val = "#"
			new[i][j] = new_val

def value(g):
	nwoods, nlumber = 0,0
	for col in grid:
		for val in col:
			if val == "|":
				nwoods += 1
			elif val == "#":
				nlumber += 1
	return nwoods * nlumber

show(grid)
g415 = None
g499 = None
print()
for i in range(500):
	updatex(grid, grid2)
	v = value(grid)
	if i % 100 == 0:
		print(i, v)
	if v >= 150000 and v < 160000:
		print("150k:",i, v)
	if i == 415:
		g415 = deepcopy(grid)
	if i == 499:
		g499 = deepcopy(grid)
	if i == 496:
		print("496:", v)
	tmp = grid
	grid = grid2
	grid2 = tmp
	
show(grid)
print(value(grid))
print("repeat?", g415 == g499)

#NB: inspection revealed period of 84 after at least 415 steps, and final count is N*84 + 415 + 81, or the same point in period as 496, output above
