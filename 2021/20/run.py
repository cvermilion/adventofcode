#data = open("input_test.txt").read()

data = open("input.txt").read()

codeStr, gridStr = data.split("\n\n")
codeStr = codeStr.replace("\n","").strip()

def val(c):
	return 1 if c == "#" else 0

code = [val(c) for c in codeStr]

grid = [[val(c) for c in l] for l in gridStr.strip().split("\n")]

def rep_grid(g):
    return "\n".join("".join("#" if n else "." for n in row) for row in g)

def nabes(i,j):
    return [
    	(i-1,j-1),
    	(i,j-1),
    	(i+1,j-1),
    	(i-1,j),
    	(i,j),
    	(i+1,j),
    	(i-1,j+1),
    	(i,j+1),
    	(i+1,j+1)
    ]

def nxt(grid,i,j):
	val = int("".join([str(grid[jj][ii]) for (ii,jj) in nabes(i,j)]), 2)
	return code[val]

def padded(N, grid):
	gx = len(grid[0])
	return (
		[[0] * (gx+2*N)] * N
		+ [[0]*N + row + [0]*N for row in grid]
		+ [[0] * (gx+2*N)] * N
	)

def do_step_test(grid):
	# could optimize by skipping over the padding area
	imax = len(grid[0])-1
	jmax = len(grid)-1
	# code[0] = 0 means the empty border stays empty
	return [[nxt(grid,i,j) if (i > 0 and j > 0 and i < imax and j < jmax) else 0 for i in range(imax+1)] for j in range(jmax+1)]
	
def do_step(grid):
	# could optimize by skipping over the padding area
	imax = len(grid[0])-1
	jmax = len(grid)-1
	# a trick for the real input: code[0] = 1 ans code[512] = 0 means
	# that the border region alternates between 0 and 1
	return [[nxt(grid,i,j) if (i > 0 and j > 0 and i < imax and j < jmax) else (1-grid[j][i]) for i in range(imax+1)] for j in range(jmax+1)]
	

#twice = do_step_test(do_step_test(padded(3, grid)))
#print("Part 1:", sum(map(sum, twice)))

twice = do_step(do_step(padded(3, grid)))
print("Part 1:", sum(map(sum, twice)))

# part 2
g = padded(51, grid)
for i in range(50):
	g = do_step(g)

print("Part 2:", sum(map(sum, g)))
