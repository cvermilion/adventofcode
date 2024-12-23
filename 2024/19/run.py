from me import *
from functools import cache

input = get_data_2024(19)

#input = input_test

towels, patterns = input.split("\n\n")
towels = towels.strip().split(", ")
patterns = patterns.strip().splitlines()

# Part 1

# greedy match: longest first
towels.sort(key=lambda t:len(t))

def can_match(pat):
	if not pat:
		return True
	for t in towels:
		if pat.startswith(t) and can_match(pat[len(t):]):
			return True
	return False

result1 = count(p for p in patterns if can_match(p))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=19)

# Part 2

@cache
def num_matches(pat):
	if not pat:
		return 1
	return sum(num_matches(pat[len(t):]) for t in towels if pat.startswith(t))

result2 = sum(num_matches(p) for p in patterns)

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=19)
