from functools import reduce

data = open("input.txt").read()
groups = data.split("\n\n")

p1_groups = [g.replace("\n", "") for g in groups]
chars = [set(g) for g in p1_groups]
print("Part 1: ", sum(len(cc) for cc in chars))

p2_groups = [[set(l) for l in g.split("\n")] for g in groups]
ints = [reduce(lambda s1,s2: s1.intersection(s2), g) for g in p2_groups]
print("Part 2: ", sum(len(i) for i in ints))



