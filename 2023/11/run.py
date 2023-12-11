from me import *
from sickos.yes import *
from itertools import *

input = get_data_2023(11)

#input = input_test

# Part A

grid = (pipeline(input.splitlines())
	| [[lambda c: 1 if c == "#" else 0]]
	| DONE
)
H,W = len(grid), len(grid[0])

empty_rows = [j for j in range(H) if not any(grid[j])]
empty_cols = [i for i in range(W) if not any(row[i] for row in grid)]

pts = [(i,j) for j in range(H) for i in range(W) if grid[j][i]]

def dist(p1, p2, expansion_factor):
	(i1,j1), (i2,j2) = p1, p2
	(i1,i2) = min(i1,i2), max(i1,i2)
	(j1,j2) = min(j1,j2), max(j1,j2)
	return (
		(i2-i1)
		+ (j2-j1)
		+ sum(expansion_factor-1 for r in empty_rows if j1 < r < j2)
		+ sum(expansion_factor-1 for c in empty_cols if i1 < c < i2)
		)

resultA = sum(dist(p1, p2, 1) for (p1,p2) in combinations(pts, 2))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=11)

# Part B

resultB = sum(dist(p1, p2, 1000000) for (p1,p2) in combinations(pts, 2))
print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=11)
