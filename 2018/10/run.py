input = open("input.txt").readlines()
from parse import parse

fmt = "position=<{x:6d}, {y:6d}> velocity=<{vx:3d}, {vy:2d}>"

pts = [parse(fmt,l) for l in input]

x = [pt["x"] for pt in pts]
y = [pt["y"] for pt in pts]
vx = [pt["vx"] for pt in pts]
vy = [pt["vy"] for pt in pts]

print(x[0], y[0], vx[0], vy[0])

num=0
den=0
for i in range(len(pts)):
	for j in range(len(pts)):
		if i == j:
			continue
		num += x[i]*(vx[i] - vx[j]) + x[j]*(vx[j]-vx[i]) + y[i]*(vy[i] - vy[j]) + y[j]*(vy[j] - vy[i])
		den += vx[i]**2 + vx[j]**2 - 2*vx[i]*vx[j] + vy[i]**2 + vy[j]**2 - 2*vy[i]*vy[j]

t_min = round(-num/den)
print(t_min)

result = [[x[i] + vx[i]*t_min, y[i]+vy[i]*t_min] for i in range(len(x))]

print(result[0])

xmin = min(r[0] for r in result)
xmax = max(r[0] for r in result)
ymin = min(r[1] for r in result)
ymax = max(r[1] for r in result)

print(xmin, xmax, ymin, ymax)

grid = [["." for j in range(xmin,xmax+1)] for i in range(ymin,ymax+1)]
print(len(grid), len(grid[0]))
for r in result:
	print(r)
	grid[r[1] - ymin][r[0] - xmin] = "#"

s = "\n".join(["".join(grid[j]) for j in range(ymax+1-ymin)])

print(s)
