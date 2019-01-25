input = open("input.txt"). readlines()
map = [[l[i] for l in input] for i in range(len(input[0]))]

class Node (object):
	def __init__(self, loc, val, neighbors):
		self.loc = loc
		self.val = val
		self.neighbors = neighbors

class Fighter (object):
	def __init__(self, typ, loc):
		self.typ = typ
		self.loc = loc
		self.hp = 200
		self.dead = False
		self.attack = 3

def neighbors(loc):
	i,j = loc
	return [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]
	
onodes = []
fighters = []
nelfs = 0
ngoblins = 0
for j in range(len(map[0])):
	for i in range(len(map)):
		map[i][j] = Node((i,j), map[i][j], [])
for j in range(1, len(map[0])-1):
	for i in range(1, len(map)-1):
		n = map[i][j]
		if n.val == "#":
			continue
		onodes.append(n)
		if n.val == "G" or n.val == "E":
			fighters.append(Fighter(n.val, n))
			if n.val == "G":
				ngoblins += 1
			else:
				nelfs += 1
		for (ii, jj) in neighbors([i,j]):
			nn = map[ii][jj]
			if nn.val != "#":
				n.neighbors.append(nn)

def is_attackable(f):
	for n in f.loc.neighbors:
		if n.val == ".":
			return True
	return False

def targets(f):
	other_type = [ff for ff in fighters if ff.typ != f.typ and not ff.dead]
	return [ff for ff in other_type if ff.loc in f.loc.neighbors or is_attackable(ff)]

def closest_target(loc, tgts):
	""" Finds the closest target Node in tgts to loc, returning a tuple of the first and last nodes in the path. """
	tgts = grid_sort(tgts)
	
	direct = [t for t in tgts if t.loc in loc.neighbors]
	if len(direct) > 0:
		return direct[0].loc, None, direct[0]
	
	tgt_locs = [t.loc for t in tgts]
	seen = set([loc])
	paths = set()
	for n in [n for n in loc.neighbors if n.val == "."]:
		seen.add(n)
		paths.add((n,n))
	possible_next = []
	while len(paths) > 0:	
		new_paths = set()
		new_seen = set()
		for p in paths:
			for l in [l for l in p[1].neighbors if not l in seen]:
				if l in tgt_locs:
					possible_next.append((p[0],l))
				else:
					new_seen.add(l)
					if l.val == ".":
						new_paths.add((p[0],l))
		seen = seen.union(new_seen)
		paths = new_paths
		if possible_next:
			return None, min(possible_next, key=lambda l:[list(reversed(l[1].loc)), list(reversed(l[0].loc))])[0], 1
	return None,None,None

def grid_sort(fs):
	return sorted(fs, key=lambda f:list(reversed(f.loc.loc)))
	
def take_turn(f):
	global nelfs, ngoblins
	direct, next, tgt = closest_target(f.loc, targets(f))
	if tgt is None:
		return
	
	if next:
		old = f.loc
		f.loc = next
		old.val = "."
		next.val = f.typ
	
	# Find weakest neighbor
	attackable = [ff for ff in fighters if ff.loc in f.loc.neighbors and not ff.dead and ff.typ != f.typ]
	if not attackable:
		return
	tgt = min(grid_sort(attackable), key=lambda ff:ff.hp)
		
	# attack target
	tgt.hp -= f.attack
	if tgt.hp <= 0:
		tgt.dead = True
		tgt.loc.val = "."
		if tgt.typ == "G":
			ngoblins -= 1
		else:
			nelfs -= 1
	
def step():
	global fighters, nelfs,ngoblins
	for f in fighters:
		if not f.dead:
			if f.typ == "G" and nelfs == 0:
				return False
			if f.typ == "E" and ngoblins == 0:
				return False
			take_turn(f)
	fighters = [f for f in fighters if not f.dead]
	fighters = grid_sort(fighters)
	return True

def show():
	print("\n".join("".join(map[i][j].val for i in range(len(map))) for j in range(len(map[0]))))

steps = 0
show()
while nelfs > 0 and ngoblins > 0:
	if not step():
		break
	steps += 1

print(steps)
show()

rem_hp = sum(f.hp for f in fighters if not f.dead)
print(rem_hp)
print(steps * rem_hp)
print([f.hp for f in fighters])
