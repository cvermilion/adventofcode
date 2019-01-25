test_input = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

from parse import parse
input=open("input.txt").readlines()
#input=test_input.splitlines()
coords = [parse("{x:d}, {y:d}", l) for l in input]
print(coords)
coords = [(c["x"],c["y"]) for c in coords]
print(coords[0])

xmax = max(c[0] for c in coords)
ymax = max(c[1] for c in coords)
print(xmax,ymax)

def show(g):
	print("\n".join(["".join([chr(65+v) for v in row]) for row in g]))

def neighbors(x,y):
	nn = set()
	if x > 0:
		nn.add((x-1, y))
	if y > 0:
		nn.add((x, y-1))
	if y < ymax:
		nn.add((x, y+1))
	if x < xmax:
		nn.add((x+1, y))
	return nn

grid = [[-2 for j in range(ymax+1)] for i in range(xmax+1)]

for i,xy in enumerate(coords):
	x,y = xy
	grid[x][y] = i

#show(grid)

current = set(coords)
seen = current.copy()

i=0
while len(current) > 0:
	nabes = set()
	for xy in current:
		x,y = xy
		nn = neighbors(x,y)
		nabes = nabes.union(nn)
	nabes = nabes - seen
	seen = seen.union(nabes)
	
	current = set()
	updates = []
	for xy in nabes:
		x,y = xy
		nn = neighbors(x,y)
		neighbor_vals = set(grid[x][y] for (x,y) in nn if grid[x][y] != -2)
		if len(neighbor_vals) > 1:
			updates.append((xy, -1))
		else:
			updates.append((xy, neighbor_vals.pop()))
		current.add(xy)
	
	for (xy, val) in updates:
		x,y = xy
		grid[x][y] = val
	#show(grid)

counts = dict((i,0) for i in range(-1, len(coords)))
for row in grid:
	for cell in row:
		counts[cell] += 1

print(counts)

infinities = set()
for y in range(ymax+1):
	infinities.add(grid[0][y])
	infinities.add(grid[xmax][y])
for x in range(xmax+1):
	infinities.add(grid[x][0])
	infinities.add(grid[x][ymax])
print(infinities)

for i in infinities:
	counts[i] = 0
print(counts)
print(max(counts.values()))
		
	
def total_dist(x,y):
	return sum(abs(x-c[0]) + abs(y-c[1]) for c in coords)

total=0
size = max([xmax+1, ymax+1])
print("size:", size)
for i in range(size):
	for j in range(size):
		if total_dist(i,j) < 10000:
			total += 1

print(total)


	
