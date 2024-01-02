from me import *
from sickos.yes import *

input = get_data_2023(18)

#input = input_test

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

#print(rep_grid(grid))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=18)

# Part B

dir_codes = [R,D,L,U]
class C:
	# consts for corners
	UL, UR, LL, LR = 0,1,2,3
	# vertical wall
	VW = 4

# line like 'R 6 (#70c710)'
def parse_line(l):
	_, _, col = parse("{} {:d} (#{})", l)
	return dir_codes[int(col[-1])], int(col[:5], 16)

dirs = [parse_line(l) for l in input.splitlines()]

# one pass to compute bounds
i,j = (0,0)
min_i = min_j = max_i = maxj = 0
for dir in dirs:
	d, n = dir
	if d == R:
		i,j = i+n, j
	elif d == L:
		i,j = i-n, j
	elif d == D:
		i,j = i, j+n
	elif d == U:
		i,j = i, j-n
	
	min_i = min(i, min_i)
	min_j = min(j, min_j)
	max_i = max(i, max_i)
	max_j = max(j, max_j)
	
i,j = (0,0)
walls = [[] for _ in range(max_j-min_j+1)]
# starting point is an upper-left corner
walls[0-min_j] = [(0, C.UL)]
prev_dir = None
for dir in dirs:
	d, n = dir
	if d == R:
		if prev_dir == U:
			walls[j-min_j].append((i, C.UL))
		elif prev_dir == D:
			walls[j-min_j].append((i, C.LL))
		else:
			if prev_dir is not None:
				assert(False)
		i,j = i+n, j
	elif d == L:
		if prev_dir == U:
			walls[j-min_j].append((i, C.UR))
		elif prev_dir == D:
			walls[j-min_j].append((i, C.LR))
		else:
			if prev_dir is not None:
				assert(False)
		i,j = i-n, j
	elif d == D:
		for jj in range(j+1, j+n):
			walls[jj-min_j].append((i, C.VW))
		if prev_dir == R:
			walls[j-min_j].append((i, C.UR))
		elif prev_dir == L:
			walls[j-min_j].append((i, C.UL))
		else:
			if prev_dir is not None:
				assert(False)
		i,j = i, j+n
	elif d == U:
		for jj in range(j-1, j-n, -1):
			walls[jj-min_j].append((i, C.VW))
		if prev_dir == R:
			walls[j-min_j].append((i, C.LR))
		elif prev_dir == L:
			walls[j-min_j].append((i, C.LL))
		else:
			if prev_dir is not None:
				assert(False)
		i,j = i, j-n
	prev_dir = d

total = 0
for (rowj, row) in enumerate(walls):
	row = list(sorted(row))
	while row:
		(cur_i, cur_typ), row = row[0], row[1:]
		end_i = cur_i
		if cur_typ == C.VW:
			# consume any LL-LR or UL-UR pairs (which count, and leave us inside the loop)
			while row:
				(nxt_i, nxt_typ), row = row[0], row[1:]
				if nxt_typ == C.VW:
					end_i = nxt_i
					break
				else:
					(nnxt_i, nnxt_typ), row = row[0], row[1:]
					match (nxt_typ, nnxt_typ):
						case (C.LL, C.LR) | (C.UL, C.UR):
							pass
						case (C.UL, C.LR) | (C.LL, C.UR):
							end_i = nnxt_i
							break
			total += (end_i-cur_i)+1
		else:
			(nxt_i, nxt_typ), row = row[0], row[1:]
			match (cur_typ, nxt_typ):
				case (C.UL, C.UR) | (C.LL, C.LR):
					total += (nxt_i-cur_i)+1
				case (C.UL, C.LR) | (C.LL, C.UR):
					# we're inside now
					while row:
						(nnxt_i, nnxt_typ), row = row[0], row[1:]
						if nnxt_typ == C.VW:
							end_i = nnxt_i
							break
						else:
							(nnnxt_i, nnnxt_typ), row = row[0], row[1:]
							match (nnxt_typ, nnnxt_typ):
								case (C.LL, C.LR) | (C.UL, C.UR):
									pass
								case (C.UL, C.LR) | (C.LL, C.UR):
									end_i = nnnxt_i
									break
					total += (end_i-cur_i)+1

resultB = total

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=18)
