input_test = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

input_test2 = """.....
..##.
..#..
.....
..##.
....."""

input = input_test

input = open("input.py").read()

grid = [list(l) for l in input.strip().split("\n")]

def rep_grid(g):
    return "\n".join("".join(row) for row in g)

def nabes(i,j):
    return [
    	(i-1,j-1),
    	(i,j-1),
    	(i+1,j-1),
    	(i-1,j),
    	(i+1,j),
    	(i-1,j+1),
    	(i,j+1),
    	(i+1,j+1)
    ]

def nabes_for_dir(i,j,dir):
	return {
		"N": [(i-1,j-1), (i,j-1), (i+1,j-1)],
		"E": [(i+1,j-1), (i+1,j), (i+1,j+1)],
		"S": [(i-1,j+1), (i,j+1), (i+1,j+1)],
		"W": [(i-1,j-1), (i-1,j), (i-1,j+1)]
	}[dir]

def no_nabes(grid, i,j):
	return all(grid[jj][ii] == "." for (ii,jj) in nabes(i,j))

def no_nabes_for_dir(grid, dir, i,j):
	return all(grid[jj][ii] == "." for (ii,jj) in nabes_for_dir(i,j,dir))

def proposed_move(i,j,dir):
	return {
		"N": (i,j-1),
		"E": (i+1,j),
		"S": (i,j+1),
		"W": (i-1,j),
	}[dir]

def padded(N, val, grid):
	gx = len(grid[0])
	return (
		[[val] * (gx+2*N)] * N
		+ [[val]*N + row + [val]*N for row in grid]
		+ [[val] * (gx+2*N)] * N
	)

grid = padded(1, ".", grid)

def proposal(grid, dirs):
	moves = []
	for j, row in enumerate(grid):
		for i, c in enumerate(row):
			if c == "#":
				if not no_nabes(grid, i, j):
					for dir in dirs:
						if no_nabes_for_dir(grid, dir, i, j):
							moves.append(((i,j), proposed_move(i,j,dir)))
							break
	return moves

def step(grid, dirs):
	prop = proposal(grid, dirs)
	if len(prop) == 0:
		return False
	all_targets = list(m[1] for m in prop)
	counts = dict((m,all_targets.count(m)) for m in set(all_targets))
	for (old,new) in prop:
		if counts[new] == 1:
			grid[old[1]][old[0]] = "."
			grid[new[1]][new[0]] = "#"
	return True

def needs_padding(grid):
	return any(c == "#" for c in grid[0] + grid[-1]) or any(grid[j][0] == "#" for j in range(len(grid))) or any(grid[j][-1] == "#" for j in range(len(grid)))
	
def size_enclosed(grid):
	minj = 0
	while all(c == "." for c in grid[minj]):
		minj += 1
	maxj = len(grid)-1
	while all(c == "." for c in grid[maxj]):
		maxj -= 1
	mini = 0
	while all(grid[j][mini] == "." for j in range(len(grid))):
		mini += 1
	maxi = len(grid[0])-1
	while all(grid[j][maxi] == "." for j in range(len(grid))):
		maxi -= 1
	return (maxi - mini + 1) * (maxj - minj + 1)

i = 0
dirs = ["N", "S", "W", "E"]
n_elves = sum(row.count("#") for row in grid)

while i < 10:
	if needs_padding(grid):
		grid = padded(1, ".", grid)
	
	i+=1
	step(grid, dirs)
	print(i)

	dirs = dirs[1:] + [dirs[0]]

print("Part 1:", size_enclosed(grid)-n_elves)

# 10 steps done, i=10

if needs_padding(grid):
		grid = padded(1, ".", grid)

while step(grid, dirs):
	if needs_padding(grid):
		grid = padded(1, ".", grid)
	
	i+=1
	print(i)
	dirs = dirs[1:] + [dirs[0]]

# Add one to i because the while check that failed did a step
print("Part 2:", i+1)
