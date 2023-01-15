import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

def cmp(x, y):
	if isinstance(x, int):
		if isinstance(y, int):
			return -1 if x < y else (0 if x == y else 1)
		else:
			return cmp([x], y)
	if isinstance(y, int):
		return cmp(x, [y])
	for (xx,yy) in zip_longest(x,y,fillvalue=None):
		if xx is None:
			return -1
		if yy is None:
			return 1
		c = cmp(xx,yy)
		if c != 0:
			return c
	# get here for cmp([], [])
	return 0

pairs = input.split("\n\n")
msgs = [[eval(a),eval(b)] for (a,b) in [p.splitlines() for p in pairs]]

print("Part 1:", sum([i+1 for (i,(a,b)) in enumerate(msgs) if cmp(a,b) != 1]))

sentinel1 = [[2]]
sentinel2 = [[6]]
lines = sum(msgs, []) + [sentinel1, sentinel2]

out = sorted(lines, key=cmp_to_key(cmp))

print("Part 2:", (out.index(sentinel1)+1)*(out.index(sentinel2)+1))
