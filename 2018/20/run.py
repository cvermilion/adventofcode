test1 = "^ENWWW(NEEE|SSE(EE|N))$"
test2 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
test3 = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
test4 = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"

class Path (object):
	def __init__(self, seg):
		self.segments = seg

class Choices (object):
	def __init__(self, ch):
		self.choices = ch # list of either single directions like 'E' or Choices
		self.active = 0
		
def build_path(s):
	if s[0] == "^":
		_, p =  build_segments(s[1:-1])
		return p
		
def build_segments(s):	
	segments = []
	while s and not s[0] in ["|", ")"]:
		while s and s[0] in ["E", "N", "S", "W"]:
			segments.append(s[0])
			s = s[1:]
		if s and s[0] == "(":
			s, ch = build_choices(s)
			segments.append(ch)
	return s, Path(segments)

def build_choices(s):
	ch = []
	s = s[1:] # initial '('
	while s[0] != ")":
		s, seg = build_segments(s)
		ch.append(seg)
		if s[0] == "|":
			s = s[1:]
	return s[1:], Choices(ch)

def build_path_loop(s):
	segment_stack = [[]]
	choices_stack = []
	while s:
		c, s = s[0], s[1:]
		if c in ["E", "N", "S", "W"]:
			segment_stack[-1].append(c)
		elif c == "(":
			choices_stack.append([])
			segment_stack.append([])
		elif c == "|":
			choices_stack[-1].append(Path(segment_stack.pop()))
			segment_stack.append([])
		elif c == ")":
			choices_stack[-1].append(Path(segment_stack.pop()))
			segment_stack[-1].append(Choices(choices_stack.pop()))
	return Path(segment_stack.pop())
		

def enumerate_paths(p):
	if p in ["E", "N", "S", "W"]:
		return [[p]]
	paths = [[]]
	if isinstance(p, Choices):
		allpaths = []
		for c in p.choices:
			cc = enumerate_paths(c)
			for ccc in cc:
				for pp in paths:
					allpaths.append(pp + ccc)
		return allpaths
	for seg in p.segments:
		allpaths = []
		ss = enumerate_paths(seg)
		for pp in paths:
			for sss in ss:
				allpaths.append(pp + sss)
		paths = allpaths
	return paths

def enumerate_paths_loop(p):
	all_paths = []
	
	path_stack = []
	remaining_segments = p.segments
	while remaining_segments:
		s, remaining_segments = remaining_segments[0], remaining_segments[1:]
		if isinstance(s, Choices):
			path_stack.append(s)
			remaining_segments = s.choices[0].segments + remaining_segments
		else:
			path_stack.append(s)
		
	all_paths.append([p for p in path_stack if isinstance(p, str)])
	
	while True:
		# work back to last Choice in path and choose next option
		for j in range(len(path_stack)-1, -1,-1):
			s = path_stack[j]
			if isinstance(s, Choices):
				if s.active != len(s.choices) - 1:
					s.active += 1
					path_stack = path_stack[:j+1]
					break
				else:
					s.active = 0
		if j == 0:
			# made it all the way back incrementing through choices
			break
		
		# now expand
		c = path_stack[-1]
		p = c.choices[c.active]
		remaining_segments = p.segments
		while remaining_segments:
			s, remaining_segments = remaining_segments[0], remaining_segments[1:]
			if isinstance(s, Choices):
				path_stack.append(s)
				remaining_segments = s.choices[0].segments + remaining_segments
			else:
				path_stack.append(s)
		
		all_paths.append([p for p in path_stack if isinstance(p, str)])
	return all_paths


input = open("input.txt").read().strip()
print(len(enumerate_paths_loop(build_path_loop(input))))

all_paths = enumerate_paths_loop(build_path_loop(input))

def deltax(p):
	return len([s for s in p if s == "E"]) - len([s for s in p if s == "W"])

def deltay(p):
	return len([s for s in p if s == "N"]) - len([s for s in p if s == "S"])

xmax = max(deltax(p) for p in all_paths)
xmin = min(deltax(p) for p in all_paths)
ymax = max(deltay(p) for p in all_paths)
ymin = min(deltay(p) for p in all_paths)

print(xmax,xmin,ymax,ymin)


grid_size = 1000
start = (500,500)

grid = [["?" for j in range(grid_size)] for i in range(grid_size)]

# definitely walls
for i in range(1,grid_size,2):
	for j in range(1,grid_size,2):
		grid[i][j] = "#"

def rep(g, rooms, i, j):
	if (i,j) in rooms:
		return "."

def show(g):
	print("\n".join("".join(grid[i][j] for i in range(grid_size)) for j in range(grid_size)))

#show(grid)

class Room (object):
	def __init__(self, loc):
		self.loc = loc
		self.connected = set()

# walk through grid marking doors
step_delta = {"N": [0,1], "S": [0,-1], "E": [1,0], "W": [-1,0]}
rooms = {start: Room(start)}
for p in all_paths:
	prev = rooms[start]
	for step in p:
		prev_loc = prev.loc
		d = step_delta[step]
		door = (prev_loc[0] + d[0], prev_loc[1] + d[1])
		next = (prev_loc[0] + 2*d[0], prev_loc[1] + 2*d[1])
		grid[door[0]][door[1]] = "-"
		grid[next[0]][next[1]] = "."
		if next in rooms:
			r = rooms[next]
		else:
			r = Room(next)
			rooms[next] = r
		
		if not r in prev.connected:
			prev.connected.add(r)
		if not prev in r.connected:
			r.connected.add(prev)
		
		prev = r

#show(grid)

# now, walk the graph breadth-first to find farthest
start_room = rooms[start]
by_dist = {0: set([start_room])}
seen = set([start_room])
to_visit = rooms[start].connected
dist = 0
while to_visit:
	dist += 1
	by_dist[dist] = to_visit
	next = set()
	for r in to_visit:
		next.update(r.connected)
	next.difference_update(seen)
	to_visit = next
	seen.update(next)

print("max dist:", max(by_dist.keys()))

far = sum(len(s) for (d,s) in by_dist.items() if d >= 1000)
print(far)
