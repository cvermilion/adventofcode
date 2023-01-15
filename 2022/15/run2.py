import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

if "--test" in sys.argv:
	row = 10
else:
	row = 2000000

t1 = time.time()

def parse_line(l):
	# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
	si, sj, bi, bj = parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", l)
	return (si, sj), (bi, bj)

pts = [parse_line(l) for l in input.splitlines()]

# a sensor point and the exclusion distance around it, forming a diamond shape in the grid
diamonds = [(s, abs(s[0] - b[0]) + abs(s[1] - b[1])) for (s,b) in pts]

# the corners of each diamond
corners = [[(si,sj+N),(si+N,sj),(si,sj-N),(si-N,sj)] for ((si,sj), N) in diamonds]

def segment(p, q):
	# work out y = mx + b form from two points
	pi, pj = p
	qi, qj = q
	m = int((qj-pj)/(qi-pi)) # always +/-1
	b = pj - m*pi
	return [m, b, p, q]

def segment_includes(l, pt):
	# assuming pt is on the line, is it inside the segment defined by l?
	m, b, p, q = l
	pi, pj = p
	qi, qj = q
	i, j = pt
	mini, maxi = min(pi,qi), max(pi,qi)
	minj, maxj = min(pj,qj), max(pj,qj)
	return not(i < mini or i > maxi or j < minj or j > maxj)

def intersection(l1, l2):
	# do two line segments intersect?
	m1, b1, p1, q1 = l1
	m2, b2, p2, q2 = l2
	if m2 == m1:
		# either no intersection or overlap, not interested in either
		return None
	x = (b2-b1)/(m1-m2)
	y = m1*x + b1
	# check: is this on both segments?
	if segment_includes(l1, (x,y)) and segment_includes(l2, (x,y)):
		return (x,y)

# all edges of all diamonds
all_segments = sum([[segment(cc[i], cc[i-1]) for i in range(4)] for cc in corners], [])

# all points where two edges intersect
ints = list(filter(lambda p:p, sum([[intersection(l1, l2) for l2 in all_segments] for l1 in all_segments], [])))

all_corners = sum(corners, [])
# all points that are either corners or intersections
all_pts = sorted(set(all_corners + ints))

# crude filter, could be better?
# a candidate is a point with at least four adjacent corners
# or region boundary intersections.
candidates = set()
for i,p in enumerate(all_pts):
	pi,pj = p
	# at least three more points within 2 rows/columns
	cnt = 0
	qs = set()
	for q in all_pts[i+1:]:
		qi,qj = q
		if qi > pi+2:
			break
		if qj >= pj-2 and qj <= pj+2:
			cnt += 1
			qs.add(q)
	# three points right of p are candidates since we're searching forward
	if cnt >= 3:
		# half-integer coordinates are possible for intersections, round up if so
		if math.floor(pi) - pi != 0:
			pi += 0.5
		for qj in [pj-1, pj, pj+1]:
			q = (pi+1, qj)
			if q not in all_pts:
				candidates.add(q)

def check(p):
	# check a candidate solution: not covered by any sensor's region'
	pi,pj = p
	for ((si,sj), N) in diamonds:
		if abs(pi-si) + abs(pj-sj) <= N:
			return False
	return True

legal = list(filter(check, candidates))
assert(len(legal) == 1)

x,y = legal[0]
print("Part 2:", int(4000000*x + y))

t2 = time.time()
#print("time:", t2-t1)
