import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
#test2()
input = get_input()

# Naturally, Planck length distances in a plane should be represented by complex numbers. 
moves = {
	"R": 1,
	"L": -1,
	"U": 1j,
	"D": -1j,
}

# T moves one of 16 ways based on distance to H, these four plus three 90 degree rotations
# (double diagonal can only happen in part 2)
basic = {
	2: 1,
	2+1j: 1+1j,
	2-1j: 1-1j,
	2+2j: 1+1j,
}
follows = dict(sum([[(k*rot, v*rot) for (k,v) in basic.items()] for rot in [1, 1j, -1, -1j]], []))

h_steps = [(l[0], int(l.strip()[2:])) for l in input.splitlines()]

H = 0j
T = 0j
visited = set([0j])

for (dir, n) in h_steps:
	for _ in range(n):
		H += moves[dir]
		if abs(H-T) >= 2:
			T += follows[H-T]
			visited.add(T)

print("Part 1:", len(visited))

rope = [0j] * 10
visited = {0j}

for (dir, n) in h_steps:
	for _ in range(n):
		rope[0] += moves[dir]
		for i in range(1,10):
			next = rope[i-1]
			knot = rope[i]
			if abs(next-knot) >= 2:
				new = knot + follows[next-knot]
				rope[i] = new
				if i == 9:
					visited.add(new)

print("Part 2:", len(visited))
