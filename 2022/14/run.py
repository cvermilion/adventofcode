import sys

input_test = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

input = input_test
input = open("input.py").read()

pairs = []
all_pts = []
for line in input.splitlines():
	pts = [(int(x), int(y)) for (x,y) in [s.split(",") for s in line.split(" -> ")]]
	pairs += list(zip(pts, pts[1:]))
	all_pts += pts

mini = min(p[0] for p in all_pts)
maxi = max(p[0] for p in all_pts)
minj = min(p[1] for p in all_pts)
maxj = max(p[1] for p in all_pts)

walls = set()
for ((i1, j1), (i2, j2)) in pairs:
	if i1 == i2:
		j1, j2 = min(j1, j2), max(j1, j2)
		for j in range(j1, j2+1):
			walls.add((i1, j))
	else:
		i1, i2 = min(i1, i2), max(i1, i2)
		for i in range(i1, i2+1):
			walls.add((i,j1))

sand = set()

def empty(i,j):
	return ((i,j) not in sand) and ((i,j) not in walls)

# womp womp, too recursive
def fill_from(i,j):
	# fills from i,j
	# returns True if we filled (i,j), False if we spilled over
	print("filling from", i, j)
	if (i,j) in sand:
		return True
	if i < mini or i > maxi:
		return False
	for (nexti,nextj) in [(i,j+1), (i-1,j+1), (i+1,j+1)]:
		if empty(nexti, nextj):
			if not fill_from(nexti, nextj):
				return False
	print("filled", i, j)
	sand.add((i,j))
	return True

# we can't go deeper, crashes Pythonista
#sys.setrecursionlimit(512)
#fill_from(500, 0)
		
def fill_next(i,j):
	# fills from top one sand
	# returns True if we filled something, False if we spilled over
	# Part 2 can go a bit lower than 1; in part 1 anything lower than maxj means we've spilled over but harmless to keep going
	if j > maxj + 2:
		return False
	while empty(i,j+1) and j <= maxj + 2:
		j+=1
	for (nexti,nextj) in [(i-1,j+1), (i+1,j+1)]:
		if empty(nexti, nextj):
			return fill_next(nexti, nextj)
	sand.add((i,j))
	return True

while fill_next(500, 0):
	pass

print("Part 1", len(sand))

# Part 2
sand = set()
# floor, too lazy to work out exact bounda
floorj = maxj + 2
for i in range(mini - maxj - 10, maxi + maxj + 10):
	walls.add((i, floorj))

while ((500, 0) not in sand) and fill_next(500, 0):
	pass

print("Part 2", len(sand))

