from parse import parse

input_test = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

input = input_test
N = 4
W = 4*N
H = 3*N

grid_text, steps_text = input.split("\n\n")

grid = list(grid_text.splitlines())

steps = []
while steps_text:
	r = parse("{:d}{}", steps_text)
	if not r:
		n = int(steps_text)
		steps.append((n, "R"))
		steps.append((0, "L")) # dummy turn after last step
		break
	n, text = r
	dir, steps_text = text[0], text[1:]
	steps.append((n,dir))


class Cell (object):
	def __init__(self, x,y,c):
		self.x = x
		self.y = y
		self.is_wall = c == "#"
		self.up = None # once set, these are a tuple of (cell, # of clockwise rotations of direction to make after moving)
		self.down = None
		self.left = None
		self.right = None

pts = [[(Cell(i,j,c) if (c != " ") else None) for (i,c) in enumerate(row)] for (j,row) in enumerate(grid)]

# set up initial connections
for j, row in enumerate(pts):
	first = None
	for i, cell in enumerate(row):
		if not cell:
			continue
		if not first:
			first = cell
		nxt = row[(i+1)%len(row)]
		if not nxt:
			nxt = first
			first = None
		nxt.left = (cell, 0)
		cell.right = (nxt, 0)

for i in range(W):
	first = None
	for j in range(H):
		if i >= len(pts[j]):
			continue
		cell = pts[j][i]
		if not cell:
			continue
		if not first:
			first = cell
		next_row = pts[(j+1)%H]
		if i >= len(next_row):
			nxt = first
		else:
			nxt = pts[(j+1)%H][i]
			if not nxt:
				nxt = first
		nxt.up = (cell, 0)
		cell.down = (nxt, 0)
		
"""
Square labeling in test data:
	
	A
BCD
  EF

boundaries are AB, AC, AF, BE, BF, CE, DF
"""

# AB
jA = 0
jB = N
for iA in range(2*N, 3*N):
	iB = 3*N - 1 - iA
	cellA = pts[jA][iA]
	cellB = pts[jB][iB]
	cellA.up = (cellB, 2)
	cellB.up = (cellA, 2)

# AC
iA = 2*N
jC = N
for jA in range(N):
	iC = N + jA
	cellA = pts[jA][iA]
	cellC = pts[jC][iC]
	cellA.left = (cellC, 3)
	cellC.up = (cellA, 1)

# AF
iA = 3*N-1
iF = 4*N-1
for jA in range(N):
	jF = 3*N - 1 - jA
	cellA = pts[jA][iA]
	cellF = pts[jF][iF]
	cellA.right = (cellF, 2)
	cellF.right = (cellA, 2)

# BE
jB = 2*N-1
jE = 3*N-1
for iB in range(N):
	iE = 3*N - 1 - iB
	cellB = pts[jB][iB]
	cellE = pts[jE][iE]
	cellB.down = (cellE, 2)
	cellE.down = (cellB, 2)

# BF
iB = 0
jF = 3*N-1
for jB in range(N, 2*N):
	iF = 5*N - 1 - jB
	cellB = pts[jB][iB]
	cellF = pts[jF][iF]
	cellB.left = (cellF, 1)
	cellF.down = (cellB, 3)

# CE
jC = 2*N-1
iE = 2*N
for iC in range(N, 2*N):
	jE = 4*N - 1 - iC
	cellC = pts[jC][iC]
	cellE = pts[jE][iE]
	cellC.down = (cellE, 3)
	cellE.left = (cellC, 1)

# DF
iD = 3*N-1
jF = 2*N
for jD in range(N, 2*N):
	iF = 5*N - 1 - jD
	cellD = pts[jD][iD]
	cellF = pts[jF][iF]
	cellD.right = (cellF, 1)
	cellF.up = (cellD, 3)

	
rot_map = {
		"R": {"R": "D", "D": "L", "L": "U", "U": "R"},
		"L": {"R": "U", "U": "L", "L": "D", "D": "R"}
	}

def do_step(cur, step):
	n, turn = step
	cell, dir = cur
	nxt = {
		"R": lambda c: c.right,
		"L": lambda c: c.left,
		"U": lambda c: c.up,
		"D": lambda c: c.down
	}
	for _ in range(n):
		next_cell, rots = nxt[dir](cell)
		if next_cell.is_wall:
			break
		cell = next_cell
		for _ in range(rots):
			dir = rot_map["R"][dir]
		
	new_dir = rot_map[turn][dir]
	return cell, new_dir

# find upper left cell
cell = None
for c in pts[0]:
	if c and not c.is_wall:
		cell = c
		break

dir = "R"
for step in steps:
	cell, dir = do_step((cell, dir), step)
	
score = 1000*(cell.y+1) + 4*(cell.x+1) + {"R":0, "D": 1, "L": 2, "U": 3}[dir]

print("Part 2 test data:", score)

