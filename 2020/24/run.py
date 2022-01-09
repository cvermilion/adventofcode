from enum import Enum
import functools, operator

class Dir(Enum):
	E = (2,0)
	W = (-2,0)
	NE = (1,1)
	NW = (-1,1)
	SE = (1,-1)
	SW = (-1,-1)

def parse_line(s):
	if not s:
		return []
	first = s[0]
	if first == "e":
		return [Dir.E] + parse_line(s[1:])
	if first == "w":
		return [Dir.W] + parse_line(s[1:])
	first, rest = s[:2], s[2:]
	return [{
		"ne": Dir.NE,
		"nw": Dir.NW,
		"se": Dir.SE,
		"sw": Dir.SW,
	}[first]] + parse_line(rest)

def add_dir(a,b):
	return a[0]+b[0], a[1]+b[1]

def sum_line(l):
	return functools.reduce(add_dir, map(lambda d: d.value, l), (0,0))

data = open("input.py").read().strip()

paths = map(parse_line, data.split("\n"))
pts = map(sum_line, paths)

black = set()
for p in pts:
	if p in black:
		black.remove(p)
	else:
		black.add(p)

print("Part 1:", len(black))

def nabes(pt):
	return set(add_dir(pt, d.value) for d in Dir)

def step(black):
	# only need to consider black tiles and their neighbors, anything else is white that stays white
	to_consider = functools.reduce(set.union, map(nabes, black), black)
	return set(
		p for p in to_consider if
		(
			(p in black and len([n for n in nabes(p) if n in black]) in [1,2]) or
			(p not in black and len([n for n in nabes(p) if n in black]) == 2)
		)
	)

for i in range(100):
	black = step(black)
	
print("Part 2:", len(black))
