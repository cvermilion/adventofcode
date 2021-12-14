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

cur = tuple("NNCB")

#data = open("input.txt").read()
#cur = tuple("HBCHSNFFVOBNOFHFOBNO")

inserts = dict((tuple(l[0]), l[1]) for l in [l.split(" -> ") for l in data.split("\n") if l])

def step(cur):
	nxt = [inserts[cur[i:i+2]] for i in range(len(cur)-1)]
	return sum(zip(cur,nxt), ()) + (cur[-1],)

for i in range(10):
	cur = step(cur)

counts = [len([a for a in cur if a == c]) for c in set(cur)]

print("Part 1:", max(counts) - min(counts))

cur = tuple("NNCB")
for i in range(40):
	cur = step(cur)

counts = [len([a for a in cur if a == c]) for c in set(cur)]

# lol no
print("Part 2:", max(counts) - min(counts))
