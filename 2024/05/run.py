from me import *
from functools import cmp_to_key
import json

input = get_data_2024(5)

#input = input_test

rules_str, seqs_str = input.split("\n\n")
rules = [[int(c) for c in l.strip().split("|")] for l in rules_str.splitlines()]

seqs = json.loads("[[{}]]".format(seqs_str.replace("\n", "],[")))

def check(seq):
	succs = dict((n, set(seq[i+1:])) for (i,n) in enumerate(seq))
	for (bef,aft) in rules:
		if bef in succs.get(aft, []):
			return False
	return True

# Part 1

result1 = sum(s[int(len(s)/2)] for s in seqs if check(s))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=5)

# Part 2

# The problem doesn't specify that the rules define a total order, but for my data I've confirmed they do -- for each sequence that isn't ordered, there is a rule for each pair of values.

succs = dict((r[0], set(rr[1] for rr in rules if rr[0] == r[0])) for r in rules)

cmp = (lambda a,b: 0 if (a==b) else (-1 if (a in succs and b in succs[a]) else 1))

tot = 0
for s in seqs:
	if not(check(s)):
		s.sort(key=cmp_to_key(cmp))
		tot += s[int(len(s)/2)]

result2 = tot

print("Part 2:", result2)
aocd.submit(result2, part="b", day=5)