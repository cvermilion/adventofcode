#!/usr/bin/env python3 

with open("input.txt") as f:
        rows = f.read().splitlines()

nums = [[int(word) for word in row.split()] for row in rows]

diffs = [max(r) - min(r) for r in nums]
ratios = [sum([[int(x/y) for y in row if (x/y == int(x/y) and x/y != 1)] for x in row], [])[0] for row in nums]

print("Part 1: {:d}".format(sum(diffs)))
print("Part 2: {:d}".format(sum(ratios)))
