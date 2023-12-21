from me import *
from functools import cache

input = get_data_2023(21)

#input = input_test

# Part A

grid = lmap(list, input.strip().split("\n"))
loc_s = input.find("S")
s_i, s_j = loc_s%(len(grid[0])+1), loc_s//(len(grid[0])+1)

def rep_grid(g):
    return "\n".join("".join(row) for row in g)

def nabes(i,j):
    return [
    	(i,j-1),
    	(i-1,j),
    	(i+1,j),
    	(i,j+1),
    ]

def padded(N, c, grid):
	gx = len(grid[0])
	return (
		[[c] * (gx+2*N)] * N
		+ [[c]*N + row + [c]*N for row in grid]
		+ [[c] * (gx+2*N)] * N
	)

grid = padded(1, "#", grid)
s_i, s_j = s_i+1, s_j+1
#print(rep_grid(grid))
#print((s_i,s_j))

@cache
def steps_away(cur, N):
	i,j = cur
	nn = set((ni,nj) for (ni,nj) in nabes(i,j) if grid[nj][ni] != "#")
	if N == 1:
		return nn
	return set.union(*(steps_away(pt, N-1) for pt in nn))

resultA = len(steps_away((s_i,s_j), 64))

#print(rep_grid(grid))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=21)

# Part B

resultB = 42

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=21)
