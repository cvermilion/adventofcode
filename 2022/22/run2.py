import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

input = get_input()
N = 50
W = 3*N
H = 4*N

grid_text, steps_text = input.split("\n\n")

grid = list(grid_text.splitlines())

steps = []
steps_text = steps_text.strip()
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

# initial connections (assumes wrapping, haven't cleaned that up)
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
Square labeling in real data:
	
 AB
 C
DE
F

boundaries are AD, AF, BC, BE, BF, CD, EF
"""

# AD
iA = N
iD = 0
for jA in range(N):
	jD = 3*N - 1 - jA
	cellA = pts[jA][iA]
	cellD = pts[jD][iD]
	cellA.left = (cellD, 2)
	cellD.left = (cellA, 2)

# AF
jA = 0
iF = 0
for iA in range(N, 2*N):
	jF = iA + 2*N
	cellA = pts[jA][iA]
	cellF = pts[jF][iF]
	cellA.up = (cellF, 1)
	cellF.left = (cellA, 3)

# BC
jB = N-1
iC = 2*N-1
for iB in range(2*N, 3*N):
	jC = iB - N
	cellB = pts[jB][iB]
	cellC = pts[jC][iC]
	cellB.down = (cellC, 1)
	cellC.right = (cellB, 3)

# BE
iB = 3*N-1
iE = 2*N-1
for jB in range(N):
	jE = 3*N - 1 - jB
	cellB = pts[jB][iB]
	cellE = pts[jE][iE]
	cellB.right = (cellE, 2)
	cellE.right = (cellB, 2)
	
# BF
jB = 0
jF = 4*N-1
for iB in range(2*N, 3*N):
	iF = iB - 2*N
	cellB = pts[jB][iB]
	cellF = pts[jF][iF]
	cellB.up = (cellF, 0)
	cellF.down = (cellB, 0)

# CD
iC = N
jD = 2*N
for jC in range(N, 2*N):
	iD = jC - N
	cellC = pts[jC][iC]
	cellD = pts[jD][iD]
	cellC.left = (cellD, 3)
	cellD.up = (cellC, 1)

# EF
jE = 3*N-1
iF = N-1
for iE in range(N, 2*N):
	jF = iE + 2*N
	cellE = pts[jE][iE]
	cellF = pts[jF][iF]
	cellE.down = (cellF, 1)
	cellF.right = (cellE, 3)
	
	
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

print("Part 2:", score)

