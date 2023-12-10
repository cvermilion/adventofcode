from me import *
from sickos.yes import *

input = get_data_2023(10)

#input = input_test
#input = open("input_test_2.txt").read()
#input = open("input_test_3.txt").read()

# Part A

# define directions
D = (0,1)
U = (0,-1)
L = (-1,0)
R = (1,0)

# each kind of corner maps from one direction to another (two possible ways)
turns = {
	"F": {U: R, L: D},
	"7": {R: D, U: L},
	"L": {D: R, L: U},
	"J": {R: U, D: L}
}

# parse the initial grid and find the S
grid = lmap(list, input.strip().split("\n"))
loc_s = input.find("S")
s_i, s_j = loc_s%(len(grid[0])+1), loc_s//(len(grid[0])+1)

def rep_grid(g):
    return "\n".join("".join(row) for row in g)

# pad a grid on all sides with N rows/columns of c
def padded(N, c, grid):
	gx = len(grid[0])
	return (
		[[c] * (gx+2*N)] * N
		+ [[c]*N + row + [c]*N for row in grid]
		+ [[c] * (gx+2*N)] * N
	)

# given current position and direction, what is next position and direction in pipe
def nxt(cur, dir, grid):
	c = grid[cur[1]][cur[0]]
	next_dir = turns.get(c, {}).get(dir, dir)
	return (cur[0]+next_dir[0], cur[1]+next_dir[1]), next_dir

# pad with non-pipe, simplifies neighbor checking
grid = padded(1, ".", grid)
s_i, s_j = s_i+1, s_j+1

# this feels kludgey: find an initial direction you can go from the S
if grid[s_j][s_i-1] in "-FL":
	dir = L
	cur = s_i-1, s_j
elif grid[s_j][s_i+1] in "-J7":
	dir = R
	cur = s_i+1, s_j
elif grid[s_j-1][s_i] in "|F7":
	dir = U
	cur = s_i, s_j-1
elif grid[s_j+1][s_i] in "|JL":
	dir = D
	cur = s_i, s_j+1

# save the initial direction for later
init_dir = dir

# go through the loop and count the steps
steps = 1
while cur != (s_i,s_j):
	cur, dir = nxt(cur, dir, grid)
	steps += 1

# Replace S with the appropriate element, based on the direction we went out of
# it and the direction we came back into it.
grid[s_j][s_i] = {
	(R,R): "-",
	(L,L): "-",
	(U,U): "|",
	(D,D): "|",
	(R,U): "F",
	(R,D): "L",
	(L,U): "7",
	(L,D): "J",
	(U,R): "J",
	(U,L): "L",
	(D,R): "7",
	(D,L): "F",
}[(init_dir, dir)]

# Farthest distance: just half the loop length.
resultA = int(steps/2)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=10)

# Part B

# For B, double the grid in each direction so we can interpolate points you can
# move through to get out: you can squeeze between pipes but not across them.
# We model this by inserting intermediate colums and rows filled with a
# different character 'o', then running through the pipe loop from A, extending
# it across the gaps. What's left is a grid where the non-interior regions are
# connected to the outside ("floodable") via spaces that are not part of the
# loop, and the number of enclosed locations is what's left, minus the loop
# itself and the 'o' fillers.

# Add intermediate rows/columns of 'o', then pad with ' ' (space). We use ' '
# to track locations reachable from the boundary without crossing the main pipe
# loop.
exp_grid = [[grid[j//2][i//2] if i%2==0 else "o" for i in range(2*len(grid[0]))] if j%2==0 else ["o"]*(2*len(grid[0])) for j in range(2*len(grid))]
exp_grid = padded(1, " ", exp_grid)

#print(rep_grid(exp_grid))

# Connect the original pipe across the extra points, and track which points are in the loop
s_i,s_j = s_i*2+1,s_j*2+1 # new location of S after extra cells and fresh padding
dir = init_dir
loop = set([(s_i,s_j)])

# Go through the pipe loop, connecting over the intermediate "o" cells where needed.
# Track all the cells in the loop for later use.
cur, dir = nxt((s_i,s_j), init_dir, exp_grid)
while cur != (s_i,s_j):
	loop.add(cur)
	if exp_grid[cur[1]][cur[0]] == "o":
		fill = "-" if dir in [L,R] else "|"
		exp_grid[cur[1]][cur[0]] = fill
	cur, dir = nxt(cur, dir, exp_grid)

#print(rep_grid(exp_grid))

# Now, mark anything reachable from 0,0; what's left is interior or the loop itself.
exp_grid[1][1] = " "
to_check = [(1,1)]
while to_check:
	i,j = to_check.pop()
	for (ni,nj) in [(i,j-1), (i-1,j),(i+1,j),(i,j+1)]:
		c = exp_grid[nj][ni]
		if c == " ":
			continue
		if (ni,nj) not in loop:
			exp_grid[nj][ni] = " "
			to_check.append((ni,nj))
			
#print(rep_grid(exp_grid))

# Result is the number of remaining non-filler points that aren't part of the loop.
resultB = sum(sum(1 if c not in " o" else 0 for c in row) for row in exp_grid) - len(loop)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=10)
