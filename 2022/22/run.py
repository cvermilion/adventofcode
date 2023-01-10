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
#input = open("input.py").read()

grid_text, steps_text = input.split("\n\n")

grid = list(grid_text.splitlines())
W = len(grid[0])
H = len(grid)

print(H)
for row in grid:
	print(len(row))
	

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
		self.up = None
		self.down = None
		self.left = None
		self.right = None

pts = [[(Cell(i,j,c) if (c != " ") else None) for (i,c) in enumerate(row)] for (j,row) in enumerate(grid)]

#pts = [(Cell(i,j,c) if (c != " ") else None) for (i,c) in enumerate([])]

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
		nxt.left = cell
		cell.right = nxt

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
		nxt.up = cell
		cell.down = nxt

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
		next_cell = nxt[dir](cell)
		if next_cell.is_wall:
			break
		cell = next_cell
		
	new_dir = {
		"R": {"R": "D", "D": "L", "L": "U", "U": "R"},
		"L": {"R": "U", "U": "L", "L": "D", "D": "R"}
	}[turn][dir]
	return cell, new_dir

cell = None
for c in pts[0]:
	if c:
		cell = c
		break

dir = "R"
for step in steps:
	cell, dir = do_step((cell, dir), step)
	
score = 1000*(cell.y+1) + 4*(cell.x+1) + {"R":0, "D": 1, "L": 2, "U": 3}[dir]

print(score)
