from me import *

input = get_data_2024(13)

input = input_test

def parse_game(s):
	pats = [
		"Button A: X+{:d}, Y+{:d}",
		"Button B: X+{:d}, Y+{:d}",
		"Prize: X={:d}, Y={:d}"
	]
	matches = [parse(p,l) for (p,l) in zip(pats, s.splitlines())]
	[(v1x, v1y), (v2x, v2y), (p1x, p1y)] = matches
	return [(v1x, v1y), (v2x, v2y), (p1x, p1y)]

games = lmap(parse_game, input.strip().split("\n\n"))

# Part 1

def parallel(v1, v2):
	return (v1[0] == 0 and v2[0] == 0) or (v1[1]*v2[0]) == (v2[1]*v1[0])

def close_enough(x):
	return abs(x-round(x)) < 0.001

def cost(game):
	v1, v2, p = game
	(v1x,v1y), (v2x,v2y) = v1, v2
	(px,py) = p
	if not parallel(v1, v2):
		# only one solution, just find and check
		# if the factors are positive integers
		# (note: all the games are actually of this type)
		na = (py - px*(v2y/v2x))/(v1y - v1x*(v2y/v2x))
		nb = (px/v2x) - (v1x*(py - px*(v2y/v2x)))/(v1y*v2x - v1x*v2y)
		if close_enough(na) and close_enough(nb) and round(na) >= 0 and round(nb) >= 0:
			return 3*round(na) + round(nb)
		return None
	if not parallel(v1, p):
		return None
	# all three are parallel, just scan over possible integer solutions
	# want largest possible nb
	dx = px
	na = 0
	while dx >= 0 and dx%v2x != 0:
		dx -= v1x
		na += 1
	if dx < 0:
		return None
	nb = int(dz/v2x)
	return 3*na + nb
		

result1 = sum(filter(lambda x: x, map(cost, games)))
print("Part 1:", result1)
#aocd.submit(result1, part="a", day=13)

# Part 2

games = [(v1,v2,(px+10000000000000,py+10000000000000)) for (v1,v2,(px,py)) in games]

result2 = sum(filter(lambda x: x, map(cost, games)))
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=13)
