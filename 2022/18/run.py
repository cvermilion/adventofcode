import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

pts = set(tuple(int(c) for c in line.split(",")) for line in input.splitlines())

def nabes(p):
	i,j,k = p
	return set([(i+1,j,k), (i-1,j,k), (i,j+1,k), (i,j-1,k), (i,j,k+1), (i,j,k-1)])

print("Part 1:", sum(len(nabes(p).difference(pts)) for p in pts))

mini = min(p[0] for p in pts)
maxi = max(p[0] for p in pts)
minj = min(p[1] for p in pts)
maxj = max(p[1] for p in pts)
mink = min(p[2] for p in pts)
maxk = max(p[2] for p in pts)

known_escape = set()
trapped = set()
unknown = set(sum([list(nabes(p).difference(pts)) for p in pts], []))

while unknown:
	now_known = set()
	to_check = set()
	for p in unknown:
		i,j,k = p
		if i < mini or i > maxi or j < minj or j > maxj or k < mink or k > maxk:
			known_escape.add(p)
			now_known.add(p)
			continue
		nn = nabes(p).difference(pts)
		if any(n in known_escape for n in nn):
			known_escape.add(p)
			now_known.add(p)
			continue
		# can't determine p, so check its neighbors
		to_check = to_check.union(nn).difference(unknown)
			
	if not now_known and not to_check:
		# didn't learn anything this pass, what's left is trapped
		trapped = unknown
		unknown = set()
	else:
		unknown.difference_update(now_known)
		unknown = unknown.union(to_check)

print("Part 2:", sum(len([n for n in nabes(p).difference(pts).difference(trapped)]) for p in pts))
