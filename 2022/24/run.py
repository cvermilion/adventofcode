from queue import PriorityQueue

input_test = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

input = input_test
input = open("input.py").read()

chars = [list(row) for row in input.splitlines()]
W = len(chars[0])-2
H = len(chars)-2

grid = [row[1:W+1] for row in chars[1:H+1]]

def rep_grid(g):
    return "\n".join("".join(row) for row in g)

horiz_blizzards = dict((j, []) for j in range(H))
vert_blizzards = dict((i,[]) for i in range(W))
for i in range(W):
	for j in range(H):
		c = grid[j][i]
		if c == ".":
			continue
		dir, offset = {
			"<": (-1, i),
			">": (1, (W-i)%W),
			"^": (-1, j),
			"v": (1, (H-j)%H)
		}[c]
		if c in ["<",">"]:
			horiz_blizzards[j].append((dir, offset))
		elif c in ["^", "v"]:
			vert_blizzards[i].append((dir, offset))

def empty(pt,t):
	# (i,j) is empty at time t
	i,j = pt
	for (dir,offset) in horiz_blizzards[j]:
		if (dir*(t-offset))%W == i:
			return False
	for (dir,offset) in vert_blizzards[i]:
		if (dir*(t-offset))%H == j:
			return False
	return True

def blizzard_at(t):
	return [["." if empty((i,j),t) else "*" for i in range(W)] for j in range(H)]

def dist(a, b):
	ai,aj = a
	bi,bj = b
	return abs(ai-bi) + abs(aj-bj)

def score(pt, goal, t):
	# best possible score from this point and time (smaller is better)
	return dist(pt, goal) + t

def nabes(pt):
	i,j = pt
	nn = []
	if j > 0:
		nn.append((i,j-1))
	if j < H-1:
		nn.append((i,j+1))
	if i > 0:
		nn.append((i-1, j))
	if i < W-1:
		nn.append((i+1,j))
	return nn

# Ok, now we can actually start looking at paths

def best_time(t0, start, end):
	states = PriorityQueue()
	seen = set()
	# start point
	states.put((score(start, end, t0), (start, t0)))
	while not states.empty():
		sc, (pt, t) = states.get()
		if pt == end:
			return t
			
		t = t+1
		# move to an empty neighbor
		for st in [(score(n, end, t), (n, t)) for n in nabes(pt) if empty(n, t)]:
			if st not in seen:
				states.put(st)
				seen.add(st)
		# wait
		st = (sc+1,(pt,t))
		if st not in seen and empty(pt, t):
			states.put(st)
			seen.add(st)

# one extra step to exit
corner = (W-1,H-1)
best = best_time(1, (0,0), corner) + 1
	
print("Part 1:", best)

# part 2

# first wait for (W-1,H-1) to be empty
t = best+1
return_t = None
while not return_t:
	while not empty(corner, t):
		t += 1

	return_t = best_time(t, corner, (0,0))
	if return_t:
		return_t += 1
	else:
		# got stuck, try going in later
		t += 1
	

t = return_t + 1
final_t = None
while not final_t:
	while not empty((0,0), t):
		t += 1

	final_t = best_time(t, (0,0), corner)
	if final_t:
		final_t += 1
	else:
		t+=1

print("Part 2:", final_t)
