depth = 9465
target = (13,704)

#examples
#depth=510
#target=(10,10)

# for part two, need a grid that goes farther than the target, since the fastest route may not be the shortest
xmax,ymax = target[0]+1+25,target[1]+1+25

# set up geologic index
geo_index = [[0 for j in range(ymax)] for i in range(xmax)]
erosion_level = [[0 for j in range(ymax)] for i in range(xmax)]

for i in range(xmax):
	geo_index[i][0] = (16807 * i)
	erosion_level[i][0] = (geo_index[i][0] + depth) % 20183
for j in range(ymax):
	geo_index[0][j] = (48271 * j)
	erosion_level[0][j] = (geo_index[0][j] + depth) % 20183
for i in range(1, xmax):
	for j in range(1, ymax):
		if (i,j) == target:
			print("hit target")
			geo_index[i][j] = 0
			#erosion_level[i][j] = 0
		else:
			geo_index[i][j] = (erosion_level[i-1][j] * erosion_level[i][j-1])
		erosion_level[i][j] = (geo_index[i][j] + depth) % 20183
#geo_index[target[0]][target[1]] = 0
#erosion_level[target[0]][target[1]] = 0

ROCKY=0
WET=1
NARROW=2

soil_types = [[erosion_level[i][j] % 3 for j in range(target[1]+1)] for i in range(target[0]+1)]

# part 1
risk = sum(sum(soil_types, []))
print(risk)

# part 2
soil_types = [[erosion_level[i][j] % 3 for j in range(ymax)] for i in range(xmax)]

class Rocky (object):
	def __init__(self):
		self.typ = ROCKY
		self.shortest_with_gear = None
		self.shortest_with_torch = None
		self.neighbors = []

class Wet (object):
	def __init__(self):
		self.typ = WET
		self.shortest_with_gear = None
		self.shortest_with_neither = None
		self.neighbors = []

class Narrow (object):
	def __init__(self):
		self.typ = NARROW
		self.shortest_with_neither = None
		self.shortest_with_torch = None
		self.neighbors = []

types = {ROCKY: Rocky, WET: Wet, NARROW: Narrow}

# build grid
grid = [[types[soil_types[i][j]]() for j in range(ymax)] for i in range(xmax)]
# connect neighbors
for i in range(xmax):
	for j in range(ymax):
		node = grid[i][j]
		if i > 0:
			node.neighbors.append(grid[i-1][j])
		if i < xmax-1:
			node.neighbors.append(grid[i+1][j])
		if j > 0:
			node.neighbors.append(grid[i][j-1])
		if j < ymax-1:
			node.neighbors.append(grid[i][j+1])

# start at origin, do breadth-1st search of paths through the grid; note that gear-switching times mean that visiting a node multiple times can lower its shortest path (a longer path can be faster), so we don't stop the search when we've seen a node before, we stop when we didn't improve the fastest path.
orig = grid[0][0]
orig.shortest_with_torch = [0, []]
orig.shortest_with_gear = [7, []]

to_visit = set([orig])
while to_visit:
	next = set()
	for n in to_visit:
		# update fastest path to its neighbors, add neighbors to next visit if the fastest path improved
		for nn in n.neighbors:
			if n.typ == ROCKY:
				if nn.typ == ROCKY:
					if n.shortest_with_torch and (not nn.shortest_with_torch or nn.shortest_with_torch[0] > n.shortest_with_torch[0]+1):
						nn.shortest_with_torch = [n.shortest_with_torch[0]+1, n.shortest_with_torch[1] + [nn]]
						next.add(nn)
					if n.shortest_with_gear and (not nn.shortest_with_gear or nn.shortest_with_gear[0] > n.shortest_with_gear[0] + 1):
						nn.shortest_with_gear = [n.shortest_with_gear[0]+1, n.shortest_with_gear[1] + [nn]]
						next.add(nn)
				elif nn.typ == WET:
					if not nn.shortest_with_neither or nn.shortest_with_neither[0] > n.shortest_with_gear[0]+8:
						nn.shortest_with_neither = [n.shortest_with_gear[0]+8, n.shortest_with_gear[1] + [nn]]
						next.add(nn)
					if not nn.shortest_with_gear or nn.shortest_with_gear[0] > n.shortest_with_gear[0] + 1:
						nn.shortest_with_gear = [n.shortest_with_gear[0]+1, n.shortest_with_gear[1] + [nn]]
						next.add(nn)
				elif nn.typ == NARROW:
					if n.shortest_with_torch and (not nn.shortest_with_torch or nn.shortest_with_torch[0] > n.shortest_with_torch[0]+1):
						nn.shortest_with_torch = [n.shortest_with_torch[0]+1, n.shortest_with_torch[1] + [nn]]
						next.add(nn)
					#min_switch = min([n.shortest_with_gear, n.shortest_with_torch], key=lambda l:l[0])
					if not nn.shortest_with_neither or nn.shortest_with_neither[0] > n.shortest_with_torch[0]+8:
						nn.shortest_with_neither = [n.shortest_with_torch[0]+8, n.shortest_with_torch[1] + [nn]]
						next.add(nn)
			elif n.typ == WET:
				if nn.typ == ROCKY:
					if n.shortest_with_gear and (not nn.shortest_with_gear or nn.shortest_with_gear[0] > n.shortest_with_gear[0] + 1):
						nn.shortest_with_gear = [n.shortest_with_gear[0]+1, n.shortest_with_gear[1] + [nn]]
						next.add(nn)
					#min_switch = min([n.shortest_with_neither, n.shortest_with_gear], key=lambda l:l[0])
					if not nn.shortest_with_torch or nn.shortest_with_torch[0] > n.shortest_with_gear[0]+8:
						nn.shortest_with_torch = [n.shortest_with_gear[0]+8, n.shortest_with_gear[1] + [nn]]
						next.add(nn)
				elif nn.typ == WET:
					if n.shortest_with_gear and (not nn.shortest_with_gear or nn.shortest_with_gear[0] > n.shortest_with_gear[0] + 1):
						nn.shortest_with_gear = [n.shortest_with_gear[0]+1, n.shortest_with_gear[1] + [nn]]
						next.add(nn)
					if n.shortest_with_neither and (not nn.shortest_with_neither or nn.shortest_with_neither[0] > n.shortest_with_neither[0] + 1):
						nn.shortest_with_neither = [n.shortest_with_neither[0]+1, n.shortest_with_neither[1] + [nn]]
						next.add(nn)
				elif nn.typ == NARROW:
					if n.shortest_with_neither and (not nn.shortest_with_neither or nn.shortest_with_neither[0] > n.shortest_with_neither[0] + 1):
						nn.shortest_with_neither = [n.shortest_with_neither[0]+1, n.shortest_with_neither[1] + [nn]]
						next.add(nn)
					#min_switch = min([n.shortest_with_neither, n.shortest_with_gear], key=lambda l:l[0])
					if not nn.shortest_with_torch or nn.shortest_with_torch[0] > n.shortest_with_neither[0]+8:
						nn.shortest_with_torch = [n.shortest_with_neither[0]+8, n.shortest_with_neither[1] + [nn]]
						next.add(nn)
			elif n.typ == NARROW:
				if nn.typ == ROCKY:
					if n.shortest_with_torch and (not nn.shortest_with_torch or nn.shortest_with_torch[0] > n.shortest_with_torch[0]+1):
						nn.shortest_with_torch = [n.shortest_with_torch[0]+1, n.shortest_with_torch[1] + [nn]]
						next.add(nn)
					#min_switch = min([n.shortest_with_neither, n.shortest_with_torch], key=lambda l:l[0])
					if not nn.shortest_with_gear or nn.shortest_with_gear[0] > n.shortest_with_torch[0]+8:
						nn.shortest_with_gear = [n.shortest_with_torch[0]+8, n.shortest_with_torch[1] + [nn]]
						next.add(nn)
				elif nn.typ == WET:
					if n.shortest_with_neither and (not nn.shortest_with_neither or nn.shortest_with_neither[0] > n.shortest_with_neither[0] + 1):
						nn.shortest_with_neither = [n.shortest_with_neither[0]+1, n.shortest_with_neither[1] + [nn]]
						next.add(nn)
					if not nn.shortest_with_gear or nn.shortest_with_gear[0] > n.shortest_with_neither[0]+8:
						nn.shortest_with_gear = [n.shortest_with_neither[0]+8, n.shortest_with_neither[1] + [nn]]
						next.add(nn)
				elif nn.typ == NARROW:
					if n.shortest_with_torch and (not nn.shortest_with_torch or nn.shortest_with_torch[0] > n.shortest_with_torch[0]+1):
						nn.shortest_with_torch = [n.shortest_with_torch[0]+1, n.shortest_with_torch[1] + [nn]]
						next.add(nn)
					if n.shortest_with_neither and (not nn.shortest_with_neither or nn.shortest_with_neither[0] > n.shortest_with_neither[0] + 1):
						nn.shortest_with_neither = [n.shortest_with_neither[0]+1, n.shortest_with_neither[1] + [nn]]
						next.add(nn)
	to_visit = next

def rep(n):
	return {ROCKY: ".", WET:
		"=", NARROW: "|"}[n.typ]

print(grid[target[0]][target[1]].shortest_with_torch[0])
					
					
