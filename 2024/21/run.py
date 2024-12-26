from me import *

input = get_data_2024(21)

#input = input_test

PointT = namedtuple("Point", "x y")
VecT = namedtuple("Vec", "x y")

class Vec(VecT):
	def mag(self):
		return abs(self.x) + abs(self.y)
	
	def __add__(self, v2):
		return Vec(self.x+v2.x, self.y+v2.y)
		
	def __mul__(self, a):
		return Vec(a*self.x, a*self.y)
	
	def decompose(self):
		# from some manual checking, this order is
		# fastest (below we swap if this order would
		# go through the gap)
		parts = []
		if self.x < 0:
			parts.append((L, -self.x))
		if self.y > 0:
			parts.append((D, self.y))
		if self.y < 0:
			parts.append((U, -self.y))
		if self.x > 0:
			parts.append((R, self.x))
		return parts
	
class Point(PointT):
	def __sub__(self, x):
		if isinstance(x, Point):
			p2 = x
			return Vec(self.x-p2.x, self.y-p2.y)
		else:
			# assume Vec
			v = x
			return Point(self.x-v.x, self.y-v.y)
	
	def __add__(self, vec):
		return Point(self.x + vec.x, self.y +vec.y)
	
class Cell(object):
	def __init__(self, point, value):
		self.point = point
		self.value = value
	
	def __str__(self):
		return "{}@({},{})".format(self.value, self.point.x, self.point.y)
	
	def __lt__(self, c):
		return self.point < c.point and (self.value is None or self.value < c.value)

class Grid(object):
	def __init__(self, grid):
		self.cells = [[Cell(Point(i,j), val) for (i,val) in enumerate(row)] for (j,row) in enumerate(grid)]
	
	def __iter__(self):
		for row in self.cells:
			for c in row:
				yield c
	
	def __str__(self):
		return "\n".join("".join(str(c.value) for c in row) for row in self.cells)
	
U,R,D,L = Vec(0,-1), Vec(1,0), Vec(0,1), Vec(-1,0)
keys = {U: "^", D: "v", R: ">", L: "<"}

numpad = Grid([["7","8","9"],["4","5","6"],["1","2","3"],[".", "0", "A"]])

numpos = dict((c.value, c.point) for c in numpad)

def numpad_pts(code):
	return [numpos["A"]] + [numpos[c] for c in code]

def moves_numpad(pts):
	# list of lists of (dir, n) pairs
	# inner list is one button move
	mvs = []
	for a,b in zip(pts, pts[1:]):
		delta = b-a
		mm = delta.decompose()
		if len(mm) == 2 and mm[0][0] == L and mm[1][0] == U and (b.x == 0 and a.y == 3):
			# reverse and up+left move that wouldnt go through the gap
			mm = mm[1], mm[0]
		if len(mm) == 2 and mm[0][0] == D and mm[1][0] == R and (a.x == 0 and b.y == 3):
			# same for right+down
			mm = mm[1], mm[0]
		mvs.append(mm)
	return mvs

def moves_keypad(pts):
	# list of lists of (dir, n) pairs
	# inner list is one button move
	mvs = []
	for a,b in zip(pts, pts[1:]):
		delta = b-a
		mm = delta.decompose()
		if len(mm) == 2 and mm[0][0] == L and mm[1][0] == D and (b.x == 0 and a.y == 0):
			# reverse and down+left move that would go through the gap
			mm = mm[1], mm[0]
		if len(mm) == 2 and mm[0][0] == U and mm[1][0] == R and (a.x == 0 and b.y == 0):
			# reverse and up+right move that would go through the gap
			mm = mm[1], mm[0]
		mvs.append(mm)
	return mvs

def seq(mvs):
	out = []
	for button in mvs:
		for mv in button:
			out += [keys[mv[0]]] * mv[1]
		out.append("A")
	return "".join(out)

keypad = Grid([[".", "^", "A"], ["<", "v", ">"]])
keypos = dict((c.value, c.point) for c in keypad)

def keypd_pts(code):
	return [keypos["A"]] + [keypos[c] for c in code]

@cache
def seq_len(s, steps):
	if not steps:
		return len(s)
	if "A" not in s[:-1]:
		nxt = seq(moves_keypad(keypd_pts(s)))
		return seq_len(nxt, steps-1)
	parts = s[:-1].split("A")
	return sum(seq_len(p+"A", steps) for p in parts)

codes = input.splitlines()
numpad_seqs = [seq(moves_numpad(numpad_pts(c))) for c in codes]

# Part 1

result1 = sum(int(codes[i][:-1])*seq_len(s, 2) for (i,s) in enumerate(numpad_seqs))

print("Part 1:", result1)
# aocd.submit(result1, part="a", day=21)

# Part 2

result2 = sum(int(codes[i][:-1])*seq_len(s, 25) for (i,s) in enumerate(numpad_seqs))

print("Part 2:", result2) 
#aocd.submit(result2, part="b", day=21)
