from me import *

input = get_data_2024(23)

input = input_test

pairs = [l.split("-") for l in input.splitlines()]

# Part 1

# construct a map of direct neighbors
neighbors = {}
for (c1,c2) in pairs:
	if s := neighbors.get(c1):
		s.add(c2)
	else:
		neighbors[c1] = {c2}
	if s := neighbors.get(c2):
		s.add(c1)
	else:
		neighbors[c2] = {c1}

triplets = set()
for c1, nabes in neighbors.items():
	for c2 in nabes:
		for c3 in nabes:
			if c3 in neighbors[c2]:
				triplets.add(tuple(sorted([c1,c2,c3])))

result1 = count(s for s in triplets if any(c for c in s if c.startswith("t")))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=23)

# Part 2

def stupet(s):
	# you know, a sorted tuple set
	# because sets aren't hashable
	return tuple(sorted(s))

def stupet_add(s, x):
	return stupet(set(s).union(set([x])))
	
groups = set()
for c1, nabes in neighbors.items():
	groups.add(stupet([c1]))
	to_add = set()
	for s in groups:
		if all(c in nabes for c in s):
			to_add.add(stupet_add(s, c1))
	groups.update(to_add)

biggest = tuple()
for s in groups:
	if len(s) > len(biggest):
		biggest = s

result2 = ",".join(biggest)
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=23)