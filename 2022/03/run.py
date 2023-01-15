import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

def score(c):
	x = ord(c)
	if x > 95:
		return x - 96
	return x - 64 + 26

lines = [list(l.strip()) for l in input.splitlines()]
items = [(set(l[:int(len(l)/2)]), set(l[int(len(l)/2):])) for l in lines]
overlap = [a.intersection(b).pop() for (a,b) in items]

print("Part 1:", sum(map(score, overlap)))

groups = [(set(lines[3*i]), set(lines[3*i+1]), set(lines[3*i+2])) for i in range(int(len(lines)/3))]

badges = [a.intersection(b).intersection(c).pop() for (a,b,c) in groups]

print("Part 2:", sum(map(score, badges)))
