from me import *
from sickos.yes import *

input = get_data_2023(22)

#input = input_test

# Part A

Xbar = namedtuple("Xbar", ["low", "high", "y", "z"])
Ybar = namedtuple("Ybar", ["low", "high", "x", "z"])
Zbar = namedtuple("Zbar", ["low", "high", "x", "y"])

# 1,0,1~1,2,1
def parse_block(l):
	((ax,ay,az), (bx,by,bz)) = (
		pipeline(l)
		| (str.split, "~")
		| [(str.split, ",")]
		| [[int]]
		| DONE
	)
	if ax != bx:
		low, high = min(ax,bx), max(ax,bx)
		return Xbar(low, high, ay, az)
	elif ay != by:
		low, high = min(ay,by), max(ay,by)
		return Ybar(low, high, ax, az)
	else:
		low, high = min(az,bz), max(az,bz)
		return Zbar(low, high, ax, ay)

blocks = lmap(parse_block, input.splitlines())

def low_pt(b):
	match b:
		case Xbar(z=zz) | Ybar(z=zz):
			return zz
		case Zbar(low=l):
			return l
		case _:
			assert(false)

def high_pt(b):
	match b:
		case Xbar(z=zz) | Ybar(z=zz):
			return zz
		case Zbar(high=h):
			return h
		case _:
			assert(false)

def drop(b, n):
	match b:
		case Xbar() | Ybar():
			return b._replace(z=b.z-n)
		case Zbar():
			return b._replace(low=b.low-n, high=b.high-n)
		case _:
			assert(false)

def σ(b):
	match b:
		case Xbar():
			xlow, xhigh = b.low, b.high
		case _:
			xlow, xhigh = b.x, b.x
	match b:
		case Ybar():
			ylow, yhigh = b.low, b.high
		case _:
			ylow, yhigh = b.y, b.y
	return set((i,j) for i in range(xlow,xhigh+1) for j in range(ylow,yhigh+1))

# sort blocks by ascending height
blocks = list(sorted(blocks, key=low_pt))

def first_blocked_by(a, b):
	# if b falls, what is the last z value it can occupy before being blocked by a? 0 if never blocked
	σa, σb = σ(a), σ(b)
	if not set.intersection(σa, σb):
		return 0
	return high_pt(a)+1

dropped = []
blocked_by = [set() for _ in blocks]
for (ib, b) in enumerate(blocks):
	stop = 1
	for (id,d) in enumerate(dropped):
		z = first_blocked_by(d, b)
		if z > stop:
			blocked_by[ib] = set([id])
			stop = z
		elif z == stop:
			blocked_by[ib].add(id)
	dropped.append(drop(b, low_pt(b)-stop))

resultA = len(blocks) - len(set(list(bs)[0] for bs in blocked_by if len(bs)==1))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=22)

# Part B

@cache
def single_blocker(i):
	# the highest block that would make this one fall, or None
	to_check = set(blocked_by[i])
	if len(to_check) == 1:
		return list(to_check)[0]
	blockers = set()
	while to_check:
		b = max(to_check)
		to_check.remove(b)
		sb = single_blocker(b)
		if sb is None:
			blockers.add(b)
		else:
			to_check.add(sb)
		if not blockers and len(to_check)==1:
			return list(to_check)[0]
		
	if len(blockers) == 1:
		return blockers.pop()
	return None

single_blockers = [single_blocker(i) for i in range(len(blocks))]

def would_fall(i):
	# all the blocks that would fall if we removed this one
	to_check = [i]
	fallen = set()
	while to_check:
		cur = to_check.pop()
		nxt = [j for j in range(len(blocks)) if single_blockers[j] == cur]
		fallen.update(set(nxt))
		to_check += nxt
	return fallen

fallen = [would_fall(i) for i in range(len(blocks))]

resultB = sum(len(f) for f in fallen)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=22)
