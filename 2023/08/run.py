from me import *
from sickos.yes import *
from itertools import cycle
import math

input = get_data_2023(8)
#input = input_test
#input = open("input_test_b.txt").read().strip()

# Part A

steps, links = input.split("\n\n")
links = dict((t, (l,r)) for (t,l,r) in (parse("{} = ({}, {})", line) for line in links.splitlines()))

def find_steps(start, links):
	cur = start
	for i, step in enumerate(cycle(steps)):
		next = links[cur][0 if step == "L" else 1]
		if next.endswith("Z"):
			# this test happens works for my part A and B, but might need to be 'next == "ZZZ"' for arbitrary input
			return i+1
		cur = next

resultA = find_steps("AAA", links)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=8)

# Part B

periods = [find_steps(start, links) for start in links.keys() if start.endswith("A")]
resultB = math.lcm(*periods)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=8)
