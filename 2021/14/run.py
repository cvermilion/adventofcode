import numpy as np
from functools import reduce
import operator

data = """CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

s = "NNCB"

data = open("input.txt").read()
s = "HBCHSNFFVOBNOFHFOBNO"

start = [s[i:i+2] for i in range(len(s)-1)]
inserts = dict((l[0], l[1]) for l in [l.split(" -> ") for l in data.split("\n") if l])
indices = dict((c, i) for (i, c) in enumerate(set("".join(inserts.keys()))))

def counts(seen, n, pair):
    if (n,pair) in seen:
        return seen[n,pair]
    if n == 0:
        result = np.zeros(len(indices))
        result[indices[pair[0]]] += 1
        result[indices[pair[1]]] += 1
        seen[(n, pair)] = result
        return result
    insert = inserts[pair]
    result = counts(seen, n-1, pair[0]+insert) + counts(seen, n-1, insert+pair[1])
    seen[n,pair] = result
    return result

def diffn(n):
    cts = reduce(operator.add, [counts({}, n, p) for p in start])
    # this double counts the interior elements: add 1 to the edges and then divide by 2
    cts[indices[s[0]]] += 1
    cts[indices[s[-1]]] += 1
    cts /= 2
    return int(max(cts) - min(cts))

print("Part 1:", diffn(10))
print("Part 2:", diffn(40))

