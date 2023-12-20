from me import *

input = get_data_2023(18)

input = input_test

# Part A

D = (0,1)
U = (0,-1)
L = (-1,0)
R = (1,0)

# line like 'R 6 (#70c710)'
def parse_line(l):
	d, n, col = parse("{} {:d} (#{:x})", l)
	return eval(d), n, col

dirs = [parse_line(l) for l in input.splitlines()]

i,j = (0,0)
pts = []
for dir in dirs:
	d, n, col = dir
	if d == R:
		pts += [(i+ii, j, col) for ii in range(1,n+1)]
	elif d == L:
		pts += [(i-ii, j, col) for ii in range(1,n+1)]
	elif d == D:
		pts += [(i, j+jj, col) for jj in range(1,n+1)]
	elif d == U:
		pts += [(i, j-jj, col) for jj in range(1,n+1)]
	i,j,_ = pts[-1]

min_i = min(i for (i,_,_) in pts)
min_j = min(j for (_,j,_) in pts)
max_i = max(i for (i,_,_) in pts)
max_j = max(j for (_,j,_) in pts)

W = (max_i-min_i) + 1
H = (max_j-min_j) + 1
g = [[None]*W for j in range(H)]
for (i,j,col) in pts:
	g[j-min_j][i-min_i] = col

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

# pad with None, then -1; will flood with -1
# leaving the only None's inside the trench
g = padded(1, None, g)
g = padded(1, -1, g)

# flood the grid
g[1][1] = -1
to_check = [(1,1)]
while to_check:
	i,j = to_check.pop()
	for (ni,nj) in nabes(i,j):
		c = g[nj][ni]
		if c is not None:
			continue
		else:
			g[nj][ni] = -1
			to_check.append((ni,nj))

resultA = sum(sum(1 for c in row if c is None or c >= 0) for row in g)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=18)

# Part B


#print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=18)
