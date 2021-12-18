import math

x0,x1,y0,y1 = 20,30,-10,-5

x0,x1,y0,y1 = 169,206,-108,-68

vys = list(range(-abs(y0), abs(y0)+1))
vxmin = math.ceil(.5 * (math.sqrt(8*x0 + 1) - 1))
vxs = list(range(vxmin, x1+1))

def test(x,y):
	return x >= x0 and x <= x1 and y >= y0 and y <= y1

best_vy = None
sols = 0
for vy0 in reversed(vys):
	for vx0 in vxs:
		x,y,vx,vy = 0,0,vx0,vy0
		while y > y0:
			x += vx
			y += vy
			vx = max(0, vx - 1)
			vy -= 1
			if test(x,y):
				if not best_vy:
					# Part 1: first one we see is best since were trying highest vy0's first'
					best_vy = vy0
				sols += 1
				break

ymax = int(best_vy*(best_vy+1)/2)
print("Part 1:", ymax)

print("Part 2:", sols)
		
