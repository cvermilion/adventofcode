from me import *

# real data
input = get_data_2024(14)
Lx,Ly = (101,103)

# test data
#input = input_test
#Lx,Ly = (11,7)

def parse_line(s):
	px,py,vx,vy = parse("p={:d},{:d} v={:d},{:d}", s)
	return (px,py), (vx,vy)

robots = lmap(parse_line, input.strip().splitlines())

def move(steps):
	return [((px+steps*vx)%Lx, (py+steps*vy)%Ly) for ((px,py),(vx,vy)) in robots]

# Part 1

moved = move(100)

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

# crude measure of how spread out the points are (lazy stddev, it was good enough)
def spread(pts):
	x = sum(px for (px,py) in pts)/len(pts)
	y = sum(py for (px,py) in pts)/len(pts)
	return sum(abs(px-x) + abs(py-y) for (px,py) in pts)

def print_robots(robots):
	grid = [["*" if (i,j) in robots else "." for i in range(Lx)] for j in range(Ly)]
	print("\n".join("".join(row) for row in grid))

# Find the step where the stars are most bunched together and guess this is the picture
# Note that the pattern repeats after Lx*Ly steps.
spreads = [spread(move(s)) for s in range(Lx*Ly)]
result2 = spreads.index(min(spreads))
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=14)

#print()
#print_robots(move(result2))

