from me import *
from sickos.yes import *

input = get_data_2023(13)

input = input_test

# Part A

patterns = [block.splitlines() for block in input.split("\n\n")]

def check_row_ref(grid, j):
	size = min(j, len(grid)-j)
	return all(grid[j-n-1] == grid[j+n] for n in range(size))

def check_col_ref(grid, i):
	size = min(i, len(grid[0])-i)
	return all(row[i-n-1] == row[i+n] for n in range(size) for row in grid)

def rep_grid(g):
	return "\n".join(g)

resultA = (
	100*sum(sum(j for j in range(1,len(g)) if check_row_ref(g,j)) for g in patterns)
	+ sum(sum(i for i in range(1,len(g[0])) if check_col_ref(g,i)) for g in patterns)
)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=13)

# Part B

def check_row_ref(grid, j):
	size = min(j, len(grid)-j)
	return sum(1 if grid[j-n-1][i] != grid[j+n][i] else 0 for i in range(len(grid[0])) for n in range(size)) == 1

def check_col_ref(grid, i):
	size = min(i, len(grid[0])-i)
	return sum(1 if row[i-n-1] != row[i+n] else 0 for n in range(size) for row in grid) == 1


resultB = (
	100*sum(sum(j for j in range(1,len(g)) if check_row_ref(g,j)) for g in patterns)
	+ sum(sum(i for i in range(1,len(g[0])) if check_col_ref(g,i)) for g in patterns)
)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=13)
