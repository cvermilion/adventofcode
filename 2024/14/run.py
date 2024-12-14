from me import *

input = get_data_2024(14)

#input = input_test

def parse_line(s):
	px,py,vx,vy = parse("p={:d},{:d} v={:d},{:d}", s)
	return (px,py), (vx,vy)

robots = lmap(parse_line, input.strip().splitlines())

# test data
Lx,Ly = (11,7)
# real data
Lx,Ly = (101,103)

# Part 1

steps = 100
moved = [((px+steps*vx)%Lx, (py+steps*vy)%Ly) for ((px,py),(vx,vy)) in robots]

midx = int((Lx-1)/2)
midy = int((Ly-1)/2)
quadA = count(filter(lambda p: p[0] < midx and p[1] < midy, moved))
quadB = count(filter(lambda p: p[0] > midx and p[1] < midy, moved))
quadC = count(filter(lambda p: p[0] < midx and p[1] > midy, moved))
quadD = count(filter(lambda p: p[0] > midx and p[1] > midy, moved))

result1 = quadA * quadB * quadC * quadD

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=14)

# Part 2

def move(steps):
	return [((px+steps*vx)%Lx, (py+steps*vy)%Ly) for ((px,py),(vx,vy)) in robots]

def has_neighbor(p, pts):
	px,py = p
	return ((px-1,py-1) in pts or
					(px,py-1) in pts or
					(px+1,py-1) in pts or
					(px-1,py) in pts or
					(px+1,py) in pts or
					(px-1,py+1) in pts or
					(px,py+1) in pts or
					(px+1,py+1) in pts)

def connected(pts):
	return all(has_neighbor(p, pts) for p in pts)
	
def balanced(moved):
	weights = [0]*Ly
	for (px,py) in moved:
		weights[py] += px - int((Lx-1)/2)
	return all(w == 0 for w in weights)

def mirror(p):
	px,py = p
	return (Lx-1-px, py)

def symmetric(moved):
	quadA = count(filter(lambda p: p[0] < midx and p[1] < midy, moved))
	quadB = count(filter(lambda p: p[0] > midx and p[1] < midy, moved))
	quadC = count(filter(lambda p: p[0] < midx and p[1] > midy, moved))
	quadD = count(filter(lambda p: p[0] > midx and p[1] > midy, moved))
	return quadA == quadB and quadC == quadD

def spread(pts):
	x = sum(px for (px,py) in pts)/len(pts)
	y = sum(py for (px,py) in pts)/len(pts)
	return sum(abs(px-x) + abs(py-y) for (px,py) in pts)

def print_robots(robots):
	grid = [["*" if (i,j) in robots else "." for i in range(Lx)] for j in range(Ly)]
	print("\n".join("".join(row) for row in grid))

# Find the step where the stars are most bunched together and guess this is the picture
spreads = [spread(move(s)) for s in range(Lx*Ly)]
result2 = spreads.index(min(spreads))
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=14)

#print()
#print_robots(move(result2))

