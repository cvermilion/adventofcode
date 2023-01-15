import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

grid = [[int(c) for c in line.strip()] for line in input.splitlines()]
N = len(grid)

paths = ([[(i,j) for i in range(0,N)] for j in range(0,N)] +
         [[(i,j) for i in range(N-1,-1,-1)] for j in range(0,N)] +
		 [[(i,j) for j in range(0,N)] for i in range(0,N)] +
		 [[(i,j) for j in range(N-1,-1,-1)] for i in range(0,N)])

seen = set()

def val(pt):
	return grid[pt[1]][pt[0]]

for p in paths:
	tallest = val(p[0])
	seen.add(p[0])
	for pt in p:
		v = val(pt)
		if v > tallest:
			seen.add(pt)
			tallest = v

print("Part 1:", len(seen))

def paths(pt):
	# all sightlines from pt
	i0, j0 = pt
	return [
		[(i, j0) for i in range(i0-1,-1,-1)],
		[(i, j0) for i in range(i0+1,N)],
		[(i0, j) for j in range(j0-1,-1,-1)],
		[(i0, j) for j in range(j0+1,N)],
		]

def score(pt):
	v = val(pt)
	tot = 1
	for path in paths(pt):
		n = 0
		for p in path:
			n += 1
			if val(p) >= v:
				break
		tot *= n
	return tot

print("Part 2:", max(sum([[score((i,j)) for j in range(N)] for i in range(N)], [])))
		
