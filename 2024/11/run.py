from me import *
from functools import cache

input = get_data_2024(11)

#input = input_test

# Part 1

@cache
def nsplit(n, steps):
	if steps == 0:
		return 1
	if n == 0:
		return nsplit(1, steps-1)
	s = str(n)
	l = len(s)
	if l%2==0:
		return nsplit(int(s[:int(l/2)]), steps-1) + nsplit(int(s[int(l/2):]), steps-1)
	return nsplit(n*2024, steps-1)

result1 = sum(nsplit(n, 25) for n in lmap(int, input.strip().split(" ")))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=11)

# Part 2

result2 = sum(nsplit(n, 75) for n in lmap(int, input.strip().split(" ")))
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=11)
