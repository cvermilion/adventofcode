fmt = "pos=<{:d},{:d},{:d}>, r={:d}"
input = open("input.txt").readlines()
from parse import parse

pts = [parse(fmt, l) for l in input]
print(pts[-1])

ptmax = max(pts, key=lambda p:p[3])
print(ptmax)

def manhattan(p1, p2):
	return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])

def in_range(pt0, pts):
	count = 0
	for pt in pts:
		if manhattan(pt, pt0) <= pt[3]:
			count += 1
	return count

#print(count)

#in_range = [0 for i in range(len(pts))]
"""
for (i,p1) in enumerate(pts):
	for (j,p2) in enumerate(pts[i+1:]):
		j = j + (i+1)
		d = manhattan(p1, p2)
		if d <= p1[3]:
			in_range[i] += 1
		if d <= p2[3]:
			in_range[j] += 1
"""

xmin = min(p[0] for p in pts)
xmax = max(p[0] for p in pts)
ymin = min(p[1] for p in pts)
ymax = max(p[1] for p in pts)
zmin = min(p[2] for p in pts)
zmax = max(p[2] for p in pts)

xd,yd,zd = xmax-xmin,ymax-ymin,zmax-zmin

print(xmin,xmax,ymin,ymax,zmin,zmax)
print(xmax-xmin,ymax-ymin,zmax-zmin)

#pts = [[p[0]-xmin,p[1]-ymin,p[2]-zmin,p[3]] for p in pts]

#max_count = max(in_range)
#max_pts = [pts[i] for i in range(len(pts)) if in_range[i] == max_count]
#print(max_pts)

# too high: 125176783
#print(min(manhattan(p, [0,0,0]) for p in max_pts))

def scaled(pts, bin_size):
	pass

# adaptive search for max in_range, note that the function is discontinuous so this may not work
step = 20000000
xbounds = (xmin, xmax)
ybounds = (ymin, ymax)
zbounds = (zmin, zmax)
max_pt = (0,0,0)
while True:
	max_c = 0
	i = xbounds[0]
	while i < xbounds[1]:
		j = ybounds[0]
		while j < ybounds[1]:
			k = zbounds[0]
			while k < zbounds[1]:
				c = in_range((i,j,k), pts)
				if c > max_c:
					max_c = c
					max_pt = (i,j,k)
				k+=step
			j+=step
		i+=step
	print(step,max_c,max_pt)
	if step == 1:
		break
	xbounds = max((max_pt[0]-2*step, xmin)), min((max_pt[0]+2*step,xmax))
	ybounds = max((max_pt[1]-2*step, ymin)), min((max_pt[1]+2*step, ymax))
	zbounds = max((max_pt[2]-2*step, zmin)), min((max_pt[2]+2*step, zmax))
	step = int(step/5) + 1
	
# now find the closest to origin that has this max_c
cur = max_pt
# binary search along diagonal to origin
outside = (xmin,ymin,zmin)
mid = (max_pt[0]+int((max_pt[0]-outside[0])/2),max_pt[1]+int((max_pt[1]-outside[1])/2),max_pt[2]+int((max_pt[2]-outside[2])/2))
i = 0
print("start, outside, mid, cur:", outside, mid, cur)
while mid != cur and i < 100:
	i+=1
	if in_range(mid, pts) == max_c:
		cur = mid
		print("closer:", cur)
	else:
		outside = mid
		print("pulling in limit:", outside)
	mid = (cur[0]+int((cur[0]-outside[0])/2), cur[1]+int((cur[1]-outside[1])/2), cur[2]+int((cur[2]-outside[2])/2))

print("binary diagonal gets us to", cur)

# that should get us close, now just step
while True:
	next = (cur[0]-1, cur[1], cur[2])
	if in_range(next, pts) == max_c:
		cur = next
	else:
		break

print("after x scan:", cur)

while True:
	next = (cur[0], cur[1]-1, cur[2])
	if in_range(next, pts) == max_c:
		cur = next
	else:
		break

print("after y scan:", cur)

while True:
	next = (cur[0], cur[1], cur[2]-1)
	if in_range(next, pts) == max_c:
		cur = next
	else:
		break

print("after z scan:", cur)

# this algorithm isnt guaranteed to give an optimal solution but it worked for me
print("total distance:", sum(cur))
