from me import *
import numpy as np

input = get_data_2023(24)
xmin = ymin = 200000000000000
xmax = ymax = 400000000000000

"""
input = input_test
xmin = ymin = 7
xmax = ymax = 27
"""

# Part A

Line = namedtuple("Line", ["x0", "y0", "z0", "vx", "vy", "vz"])

# 19, 13, 30 @ -2,  1, -2
def parse_line(l):
	return Line(*parse("{:d}, {:d}, {:d} @ {:d}, {:d}, {:d}", l))

def intersection_bad(l1, l2):
	# what time t do these lines intersect at in x,y
	if l1.vx == l2.vx:
		assert(l1.x0 != l2.x0) # assume we don't need to consider this case
		return None
	tx = (l1.x0 - l2.x0)/(l2.vx - l1.vx)
	if tx < 0:
		return None
	if l1.vy == l2.vy:
		assert(l1.y0 != l2.y0) # assume we don't need to consider this case
		return None
	ty = (l1.y0 - l2.y0)/(l2.vy - l1.vy)
	if ty < 0:
		return None
	print(tx,ty)
	return tx if tx == ty else None

def intersection(l1, l2):
	den = (l1.vx*l2.vy - l1.vy*l2.vx)
	if den == 0:
		#print("parallel")
		return None
	# x of intx pt
	x = (l1.vx*l2.vy*l2.x0 - l2.vx*l1.vy*l1.x0 + l1.vx*l2.vx*(l1.y0-l2.y0))/den
	y = l1.y0 + (l1.vy/l1.vx)*(x - l1.x0)
	t1 = (x - l1.x0)/l1.vx
	t2 = (x - l2.x0)/l2.vx
	#print(x,y,t1,t2)
	if t1 > 0 and t2 > 0 and (xmin <= x <= xmax) and (ymin <= y <= ymax):
		return (x,y)
	return None

lines = lmap(parse_line, input.splitlines())

n = 0
for (i, li) in enumerate(lines):
	for lj in lines[i+1:]:
		xy = intersection(li, lj)
		if xy is not None:
			n += 1

resultA = n

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=24)

# Part B

# Define the thrown rock as having position s + u t (s and u 3-vectors) and each hailstone as having position
# r_i + v_i * t_i at collision (each collision time is distinct).
#
# Thus there are six "global" unknowns (velocity and initial position of the rock) and one "local" unknown per
# hailstone (t_i, the time of collision). Setting positions equal yields three constraints per line, so three
# hailstone intersections are sufficient to solve the system.
# 
# Doing this directly is quite tedious, though, and we can find some simpler constraints by observing that two
# equal vectors have null cross product:
#
#   (s + u t_i) = (r_i + v_i t_i)
#   (s - r_i) = - (u - v_i) t_i
#   (s - r_i) x (u - v_i) = 0
#   (s x u) - (r_i x u) - (s x v_i) + (r_i x v_i) = 0
#
# The (s x u) term is the same for any hailstone, so we can eliminate it by subracting the equations for two different
# hailstones:
#
#   - (r_i x u) - (s x v_i) + (r_i x v_i) + (r_j x u) + (s x v_j) - (r_j x v_j) = 0
#
# Note that this holds for any pair of hailstones. We've eliminated the irrelavent t_i, so we're left with the six
# real unknowns, and two pairs of {i,j} will suffice. For simplicity, we take {0,1} and {0,2}, and shift coordinates
# so that r_0 = 0.
#
# For faster input on my phone, I labeled the vectors:
#
# (a, b, c, d, e, f) = (v_0, v_1, v_2, r_0, r_1, r_2)
#

V3 = namedtuple("V3", ["x", "y", "z"])

# v0
a = V3(lines[0].vx, lines[0].vy, lines[0].vz)
# v1
b = V3(lines[1].vx, lines[1].vy, lines[1].vz)
# v2
c = V3(lines[2].vx, lines[2].vy, lines[2].vz)
# r1 - r0
e = V3(lines[1].x0 - lines[0].x0, lines[1].y0 - lines[0].y0, lines[1].z0 - lines[0].z0)
# r2 - r0
f = V3(lines[2].x0 - lines[0].x0, lines[2].y0 - lines[0].y0, lines[2].z0 - lines[0].z0)

A = np.array([
	[-e.y, e.x, 0, (b.y-a.y), (a.x-b.x), 0],
	[0, -e.z, e.y, 0, (b.z-a.z), (a.y-b.y)],
	[-e.z, 0, e.x, (b.z-a.z), 0, (a.x-b.x)],
	[-f.y, f.x, 0, (c.y-a.y), (a.x-c.x), 0],
	[0, -f.z, f.y, 0, (c.z-a.z), (a.y-c.y)],
	[-f.z, 0, f.x, (c.z-a.z), 0, (a.x-c.x)]
])

B = np.array([
		(e.x*b.y - e.y*b.x),
		(e.y*b.z - e.z*b.y),
		(e.x*b.z - e.z*b.x),
		(f.x*c.y - f.y*c.x),
		(f.y*c.z - f.z*c.y),
		(f.x*c.z - f.z*c.x),
])

sol = np.linalg.solve(A, B)
ux,uy,uz,sx,sy,sz = sol
sx += lines[0].x0
sy += lines[0].y0
sz += lines[0].z0

resultB = sx+sy+sz

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=24)

# yields 761691907059630.2 in Pythonista, but 761691907059631.0 (correct) on
# laptop -- need to check precision could assume result is close and all
# integers, see which rounding minimizes error or just check the interceptions
# and search around the approximate answer
