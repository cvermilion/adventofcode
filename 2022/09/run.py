input_test = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

input_test2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

#input = input_test2
input = open("input.py").read()

# Naturally, Planck length distances in a plane should be represented by complex numbers. 
moves = {
	"R": 1,
	"L": -1,
	"U": 1j,
	"D": -1j,
}

# T moves one of 16 ways based on distance to H, these three plus three 90 degree rotations (double diagonal can only happen in part 2)
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

print(len(visited))

# part 2

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

print(len(visited))
