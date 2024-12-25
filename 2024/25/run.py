from me import *
import itertools

input = get_data_2024(25)

input = input_test

KEY, LOCK = 0,1

def parse_grid(s):
	data = lmap(list, s.strip().splitlines())
	H = len(data)
	kind = KEY if data[0][0] == "." else LOCK
	data = transpose(data)
	return H, kind, [count(c for c in row if c == "#")-1 for row in data]

grids = lmap(parse_grid, input.split("\n\n"))
H = grids[0][0]

def can_fit(lock, key):
	return all(l+k <= H-2 for (l,k) in zip(lock, key))

# Part 1

locks = [l for (_, kind, l) in grids if kind == LOCK]
keys = [l for (_, kind, l) in grids if kind == KEY]

result1 = count(1 for (l,k) in itertools.product(locks, keys) if can_fit(l,k))
print("Part 1:", result1)
#aocd.submit(result1, part="a", day=25)