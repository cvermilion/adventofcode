import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

elves = input.split("\n\n")
cals = [[int(c) for c in e.splitlines()] for e in elves]

totals = [sum(cs) for cs in cals]

print("Part 1:", max(totals))
print("Part 2:", sum(sorted(totals, reverse=True)[:3]))
