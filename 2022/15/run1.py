import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

if "--test" in sys.argv:
	row = 10
else:
	row = 2000000

def parse_line(l):
	# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
	si, sj, bi, bj = parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", l)
	return (si, sj), (bi, bj)

def excluded(row, s, b):
	dist = abs(s[0] - b[0]) + abs(s[1] - b[1])
	if abs(row - s[1]) >= dist:
		return None
	diff = dist - abs(row - s[1])
	return [s[0] - diff, s[0] + diff]

pts = [parse_line(l) for l in input.splitlines()]
beacons = set(p[1] for p in pts)
bands = [excluded(row, s, b) for (s,b) in pts]

# now remove overlaps
bands = list(filter(lambda x: x, bands))
bands = sorted(bands)
distinct = [bands[0]]
for (l1,r1) in bands[1:]:
	l0,r0 = distinct[-1]
	# total overlap
	if r1 <= r0:
		continue
	# no overlap
	if l1 > r0:
		distinct.append([l1,r1])
	# some overlap
	else:
		distinct[-1][1] = r1

total = sum(r-l+1 for (l,r) in distinct)

nb = len(list(filter(lambda b: b[1] == row, beacons)))

print("Part 1:", total-nb)
