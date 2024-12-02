from me import *

input = get_data_2024(2)

#input = input_test

# Part 1

def parse_line(s):
	return [int(c) for c in s.strip().split(" ")]

def diffs(l):
	return [x-y for x,y in zip(l[1:], l)]

def check(l):
	l = diffs(l)
	return all(n in set([1,2,3]) for n in l) or all(n in set([-1,-2,-3]) for n in l)
	
reports = [parse_line(l) for l in input.splitlines()]

result1 = count(filter(check, reports))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=2)

# Part 2

def check1(l):
	if check(l):
		return True
	for i in range(len(l)):
		if check(l[:i] + l[i+1:]):
			return True
	return False

result2 = count(filter(check1, reports))

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=2)
