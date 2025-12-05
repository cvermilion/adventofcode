from me import *
from sickos.yes import *

DAY=5

input = get_data_2025(DAY)

input = input_test

ranges, ingredients = input.split("\n\n")
ranges = (pipeline(ranges.splitlines())
  | [(str.split, "-")]
  | [[int]]
  | DONE)
ingredients = lmap(int, ingredients.splitlines())

# Part 1

def fresh(i):
	for l,h in ranges:
		if i >= l and i <= h:
			return True
	return False

result1 = count(i for i in ingredients if fresh(i))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=DAY)

# Part 2

def intersect(r1, r2):
	r1l, r1h = r1
	r2l, r2h = r2
	return ((r2l >= r1l and r2l <= r1h) or
	    (r2h >= r1l and r2h <= r1h) or
	    (r1l >= r2l and r1l <= r2h) or
	    (r1h >= r2l and r1h <= r2h))

unique = []
to_check = ranges
while to_check:
	r = to_check.pop()
	intersected = False
	for u in to_check:
		if intersect(r, u):
			u[0] = min(r[0], u[0])
			u[1] = max(r[1], u[1])
			intersected = True
			break
	if not intersected:
		unique.append(r)
			
result2 = sum(h-l+1 for (l,h) in unique)
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=DAY)
