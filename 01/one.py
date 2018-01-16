#!/usr/bin/env python3

with open("input.txt") as f:
    nstr = f.read().strip()

digs = list(map(int, nstr))

# digits that match the next digit
dupes1 = [n for (i, n) in enumerate(digs) if list(digs)[(i+1)%len(digs)] == n]

# digits that match the digit halfway around the (circular) list
dupes2 = [n for (i, n) in enumerate(digs) if list(digs)[(i+int(len(digs)/2))%len(digs)] == n]

print("Part 1: {:d}".format(sum(dupes1)))
print("Part 2: {:d}".format(sum(dupes2)))

