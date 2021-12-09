import functools
import operator

data = """2199943210
3987894921
9856789892
8767896789
9899965678"""

data = open("input.txt").read().strip()

# Simplify the indexing by wrapping two sides with '10' values, and then using wraparound indexing.
grid = [[int(c) for c in l] + [10] for l in data.split("\n")]
grid += [[10 for i in range(len(grid[0]))]]

def min_nabe(g,i,j):
	nx = len(g[0])
	ny = len(g)
	pts = [((i+1) % nx, j), ((i-1+nx)%nx, j), (i, (j+1)%ny), (i, (j-1+ny)%ny)]
	return min([(x,y,g[y][x]) for (x,y) in pts], key=lambda p:p[2])

part1 = sum([sum([grid[j][i]+1 for i in range(len(grid[j])) if grid[j][i] < min_nabe(grid, i, j)[2]]) for j in range(len(grid))])

print("Part 1:", part1)

pts = functools.reduce(operator.add, [[(x,y) for x in range(len(grid[0]))] for y in range(len(grid))])
basins = dict([(p,p) for p in pts if grid[p[1]][p[0]] < min_nabe(grid, p[0], p[1])[2]])
basin_members = dict((p, set([p])) for p in basins.keys())

def find_basin(basins, p):
	if p in basins:
		return basins[p]
	if grid[p[1]][p[0]] >= 9:
		return None
	x,y,_ = min_nabe(grid, p[0], p[1])
	b = find_basin(basins, (x,y))
	basins[p] = b
	return b

for p in pts:
	b = find_basin(basins, p)
	if b:
		basin_members[b].add(p)

sizes = sorted([len(mem) for mem in basin_members.values()])
print(functools.reduce(operator.mul, sizes[-3:]))
