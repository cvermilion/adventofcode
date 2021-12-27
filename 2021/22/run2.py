data = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".splitlines()

data = open("input.py").readlines()

from parse import parse
from typing import NamedTuple

class Cuboid(NamedTuple):
	x1: int
	x2: int
	y1: int
	y2: int
	z1: int
	z2: int
	on: bool
	
def cuboid(s):
	r = parse("{sgn} x={x1:d}..{x2:d},y={y1:d}..{y2:d},z={z1:d}..{z2:d}", s)
	x1,x2 = sorted([r["x1"], r["x2"]])
	y1,y2 = sorted([r["y1"], r["y2"]])
	z1,z2 = sorted([r["z1"], r["z2"]])
	on = r["sgn"] == "on"
	return Cuboid(x1,x2,y1,y2,z1,z2,on)

instrs = [c for c in map(cuboid, data) if c]

def has_intersection(c1, c2):
	return (
		(c1.x2 >= c2.x1 and c1.x1 <= c2.x2)
		and (c1.y2 >= c2.y1 and c1.y1 <= c2.y2)
		and (c1.z2 >= c2.z1 and c1.z1 <= c2.z2)
		)

def coversx(c1, c2):
	return c2.x1 >= c1.x1 and c2.x2 <= c1.x2

def coversy(c1, c2):
	return c2.y1 >= c1.y1 and c2.y2 <= c1.y2

def coversz(c1, c2):
	return c2.z1 >= c1.z1 and c2.z2 <= c1.z2

def covers(c1, c2):
	return (coversx(c1, c2) and coversy(c1, c2) and coversz(c1, c2))

def size(c):
	return (c.x2-c.x1+1) * (c.y2-c.y1+1) * (c.z2-c.z1+1)

def splitx(c, s):
	return Cuboid(c.x1, s, c.y1, c.y2, c.z1, c.z2, c.on), Cuboid(s+1, c.x2, c.y1, c.y2, c.z1, c.z2, c.on)

def splity(c, s):
	return Cuboid(c.x1, c.x2, c.y1, s, c.z1, c.z2, c.on), Cuboid(c.x1, c.x2, s+1, c.y2, c.z1, c.z2, c.on)

def splitz(c, s):
	return Cuboid(c.x1, c.x2, c.y1, c.y2, c.z1, s, c.on), Cuboid(c.x1, c.x2, c.y1, c.y2, s+1, c.z2, c.on)

def add(c1, c2):
	# return a list of non-overlapping cuboids
	# we split one cuboid until only
	# fully overlapping or non-overlapping
	# cuboids remain
	if not c1.on:
		assert(false)
	if covers(c1, c2) and c2.on:
		return [c1]
	if covers(c2, c1):
		if c2.on:
			return [c2]
		else:
			return []
	if not has_intersection(c1, c2):
		if c2.on:
			return [c1, c2]
		else:
			return [c1]
	
	if not (c2.on and coversx(c1,c2)) and not coversx(c2,c1):
		if c1.x1 == c2.x1:
			split = c2.x2
			c3,c4 = splitx(c1, split)
			return [c4] + add(c3, c2)
		elif c1.x1 > c2.x1:
			split = c2.x2
			c3,c4 = splitx(c1, split)
			return [c4] + add(c3, c2)
		else:
			split = c2.x1-1
			c3,c4 = splitx(c1, split)
			return [c3] + add(c4, c2)
	
	if not (c2.on and coversy(c1,c2)) and not coversy(c2,c1):
		if c1.y1 == c2.y1:
			split = c2.y2
			c3,c4 = splity(c1, split)
			return [c4] + add(c3, c2)
		elif c1.y1 > c2.y1:
			split = c2.y2
			c3, c4 = splity(c1, split)
			return [c4] + add(c3, c2)
		else:
			split = c2.y1-1
			c3,c4 = splity(c1, split)
			return [c3] + add(c4, c2)
			
	if not (c2.on and coversz(c1,c2)) and not coversz(c2,c1):
		if c1.z1 == c2.z1:
			split = c2.z2
			c3,c4 = splitz(c1, split)
			return [c4] + add(c3, c2)
		elif c1.z1 > c2.z1:
			split = c2.z2
			c3,c4 = splitz(c1, split)
			return [c4] + add(c3, c2)
		else:
			split = c2.z1-1
			c3,c4 = splitz(c1, split)
			return [c3] + add(c4, c2)
	
	# special case: one covers the other om all three axes but not the same one. Find the cuboid that only covers rhe other on one axis and split that one on both sides.
	c1covers = []
	c2covers = []
	if coversx(c1, c2):
		c1covers.append("x")
	else:
		c2covers.append("x")
	if coversy(c1, c2):
		c1covers.append("y")
	else:
		c2covers.append("y")
	if coversz(c1, c2):
		c1covers.append("z")
	else:
		c2covers.append("z")
	assert(len(c1covers) + len(c2covers) == 3)
	
	tosplit, other = c2,c1
	axis = c2covers[0]
	if len(c1covers) == 1:
		tosplit, other = c1,c2
		axis = c1covers[0]
	
	splitoff = []
	rest = tosplit
	if axis == "x":
		if tosplit.x1 < other.x1:
			left, rest = splitx(rest, other.x1-1)
			splitoff.append(left)
		if tosplit.x2 > other.x2:
			rest, right = splitx(rest, other.x2)
			splitoff.append(right)
	elif axis == "y":
		if tosplit.y1 < other.y1:
			left, rest = splity(rest, other.y1-1)
			splitoff.append(left)
		if tosplit.y2 > other.y2:
			rest, right = splity(rest, other.y2)
			splitoff.append(right)
	else:
		assert(axis == "z")
		if tosplit.z1 < other.z1:
			left, rest = splitz(rest, other.z1-1)
			splitoff.append(left)
		if tosplit.z2 > other.z2:
			rest, right = splitz(rest, other.z2)
			splitoff.append(right)
	
	# finally, make sure we put the on cuboid first
	splitoff = [c for c in splitoff if c.on]
	if rest.on:
		return splitoff + add(rest, other)
	else:
		return splitoff + add(other, rest)

def addn(cs):
	if not cs:
		return []
	# first: keep a set of on cubes and apply each operation to all of them. Note that the rwsulting set is not disjoint.
	on = set([cs[0]])
	for c in cs[1:]:
		nxt = set([])
		for ci in on:
			nxt = nxt.union(set(add(ci, c)))
		on = nxt
	
	# now: reduce by adding any pairs of intersecting cuboids
	cc = list(on)
	out = []
	while cc:
		first, rest = cc[0], cc[1:]
		for i, c in enumerate(rest):
			if has_intersection(first, c):
				split = add(first, c)
				cc = split + rest[:i] + rest[i+1:]
				break
		else:
			out.append(first)
			cc = rest
		# first doesnt intersect anything
	return out

cc = addn(instrs)
print(sum(map(size, cc)))

