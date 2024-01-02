from me import *
from queue import PriorityQueue
from math import floor

input = get_data_2023(21)

#input = input_test

# Part A

D = (0,1)
U = (0,-1)
L = (-1,0)
R = (1,0)

grid = lmap(list, input.strip().split("\n"))
loc_s = input.find("S")
s_i, s_j = loc_s%(len(grid[0])+1), loc_s//(len(grid[0])+1)

def rep_grid(g):
    return "\n".join("".join(row) for row in g)

def nabes(i,j):
    return [
    	(i,j-1),
    	(i-1,j),
    	(i+1,j),
    	(i,j+1),
    ]

def padded(N, c, grid):
	gx = len(grid[0])
	return (
		[[c] * (gx+2*N)] * N
		+ [[c]*N + row + [c]*N for row in grid]
		+ [[c] * (gx+2*N)] * N
	)

grid = padded(1, "#", grid)
s_i, s_j = s_i+1, s_j+1

H, W = len(grid), len(grid[0])

# matrix of shortest distance to the corresponding point in grid
shortest = [[None]*W for _ in range(H)]
def rep_shortest(g):
    return "\n".join(" ".join("{:2d}".format(n) if n is not None else "xx" for n in row) for row in g)

to_check = PriorityQueue()
to_check.put((0, s_i,s_j))
while not to_check.empty():
	d,i,j = to_check.get()
	if shortest[j][i] is not None and d>=shortest[j][i]:
		continue
	shortest[j][i] = d
	for (ii,jj) in nabes(i,j):
		if grid[jj][ii] != "#":
			to_check.put((d+1,ii,jj))

#print(rep_shortest(shortest))

resultA = sum(sum(1 for n in row if n is not None and n <= 6 and n%2==0) for row in shortest)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=21)

# Part B

grid = lmap(list, input.strip().split("\n"))
loc_s = input.find("S")
s_i, s_j = loc_s%(len(grid[0])+1), loc_s//(len(grid[0])+1)
H, W = len(grid), len(grid[0])

# expand to GxG
# With trial and error, 7x7 is enough for the shortest path to a point in one
# tile to consistently be the distance to the corresponding point in a closer
# tile plus T (where T is the size of the square grid tile, 11 in the example
# data and 131 in the real data).
G = 7
grid = [row*G for row in grid]*G
T = H # period in either direction
H *= G
W *= G
# put S in middle tile
s_i += (G-1)//2*T
s_j += (G-1)//2*T

grid = padded(1, "#", grid)
s_i, s_j = s_i+1, s_j+1
H += 2
W += 2

shortest = [[None]*W for _ in range(H)]

# fil out the shortest distance in the full GxG tile gride
to_check = PriorityQueue()
to_check.put((0, s_i,s_j))
while not to_check.empty():
	d,i,j = to_check.get()
	if shortest[j][i] is not None and d>=shortest[j][i]:
		continue
	shortest[j][i] = d
	for (ii,jj) in nabes(i,j):
		if grid[jj][ii] != "#":
			to_check.put((d+1,ii,jj))

#print(rep_shortest(shortest))

# Now, iterate over the GxG tile and for every edge and corner tile, compute
# the number of periods you can go out, as a multiplicity factor.

# From an edge, go out in a line; from a corner, go out in both directions.

# Note that a point is reachable from S if it's shortest distance is <=
# steps_max *and* it's even/oddness matches steps_max.

steps_max = 26501365
#steps_max = 5000
total = 0
for t_i in range(G):
	for t_j in range(G):
		for i in range(T):
			for j in range(T):
				# add 1 for each dir for padding
				d = shortest[t_j*T + j + 1][t_i*T + i + 1]
				if d is None or d > steps_max:
					continue
				N = 0
				if t_i%(G-1) == t_j%(G-1) == 0:
					# corners
					if d%2 == steps_max%2:
						# this point has same evenness as steps_max: count this
						# point plus every point an even number of tiles away
						# (sum over two directions out from the corner)
						p = 2*int((steps_max-d)/(2*T))
						N = ((p+2)**2)//4
					else:
						# opposite evenness, count points T, 3T, etc. away
						p = int((steps_max-d)/(T))
						if p == 0:
							N = 0
						else:
							p = 1+2*floor((p-1)/2) # largest odd integer <= p
							N = (p+1)*(p+3)//4
				elif t_i%(G-1) == 0 or t_j%(G-1) == 0:
					# edges
					if d%2 == steps_max%2:
						p = int((steps_max-d)/(2*T))
						N = 1 + p
					else:
						p = int((steps_max-d+T)/(2*T))
						N = p
				else:
					# interior, just count this point if the parity is right
					if d%2 == steps_max%2:
						N = 1
				total += N
				
resultB = total

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=21)
