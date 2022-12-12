input_test = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

input = input_test

input = open("input.py").read()

grid = [[{"S": -1, "E": 42}.get(c, ord(c)-96) for c in l] for l in input.strip().split("\n")]

def rep_grid(g):
    return "\n".join("".join(chr(n+96) if n <= 26 else "#" for n in row) for row in g)

def nabes(i,j):
    return [
    	(i,j-1),
    	(i-1,j),
    	(i+1,j),
    	(i,j+1),
    ]

def reachable_nabes(pts, reverse=False):
	res = set()
	for (i,j) in pts:
		h = grid[j][i]
		for (ni,nj) in nabes(i,j):
			hn = grid[nj][ni]
			if (not reverse and hn <= h+1) or (reverse and hn >= h-1):
				res.add((ni,nj))
	return res

def padded(N, val, grid):
	gx = len(grid[0])
	return (
		[[val] * (gx+2*N)] * N
		+ [[val]*N + row + [val]*N for row in grid]
		+ [[val] * (gx+2*N)] * N
	)

# pad twice so lazy searching doesn't escape in either direction
grid = padded(1, 30, grid)
grid = padded(1, 0, grid)

# find the start and end (note padding shifts these but it doesn't matter)
starti, startj = None, None
endi, endj = None, None
for j in range(len(grid)):
	for i in range(len(grid[j])):
		if grid[j][i] == 42:
			grid[j][i] = 26
			endi, endj = i,j
		elif grid[j][i] == -1:
			grid[j][i] = 0
			starti, startj = i,j

scores = [[None for i in range(len(row))] for row in grid]
scores[startj][starti] = 0
cur = [(starti, startj)]
steps = 0

while scores[endj][endi] is None:
	steps += 1
	nxt = set()
	for (ni,nj) in reachable_nabes(cur):
		if scores[nj][ni] is None:
			scores[nj][ni] = steps
			nxt.add((ni,nj))
	cur = nxt

print("Part 1:", scores[endj][endi])

# part 2: same algorithm run backward until we hit an 'a'
cur = set([(endi,endj)])
scores = [[None for i in range(len(row))] for row in grid]
steps = 0
res = None

while not res:
	steps += 1
	nxt = set()
	for (ni,nj) in reachable_nabes(cur, True):
		if grid[nj][ni] == 1:
			res = steps
			break
		if scores[nj][ni] is None:
			scores[nj][ni] = steps
			nxt.add((ni,nj))
	cur = nxt

print("Part 2:", res)
