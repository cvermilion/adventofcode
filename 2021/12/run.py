data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

data = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

data = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

data = """LP-cb
PK-yk
bf-end
PK-my
end-cb
BN-yk
cd-yk
cb-lj
yk-bf
bf-lj
BN-bf
PK-cb
end-BN
my-start
LP-yk
PK-bf
my-BN
start-PK
yk-EP
lj-BN
lj-start
my-lj
bf-LP"""

pairs = [l.split("-") for l in data.split("\n")]
pts = set([p[0] for p in pairs] + [p[1] for p in pairs])
nabes = dict((p, set([])) for p in pts)
for (p1, p2) in pairs:
	if p2 != "start":
		nabes[p1].add(p2)
	if p1 != "start":
		nabes[p2].add(p1)

def lower(p):
	return ord(p[0]) > 90

def paths(remaining, sofar):
	last = sofar[-1]
	if last == "end":
		return [sofar]
	nxt = nabes[sofar[-1]] & remaining
	branches = [paths((remaining - set([n]) if lower(n) else remaining), sofar + [n]) for n in nxt]
	return sum(branches, [])

print("Part 1:", len(paths(pts - set(["start"]), ["start"])))

def paths2(remaining, used_double, sofar):
	last = sofar[-1]
	if last == "end":
		return [sofar]
	nxt = nabes[sofar[-1]] & remaining
	branches = [paths2((remaining - set([n]) if lower(n) else remaining), used_double, sofar + [n]) for n in nxt]
	if not used_double:
		doubles = nabes[sofar[-1]] - remaining
		branches += [paths2(remaining, True, sofar + [n]) for n in doubles]
	return sum(branches, [])
	
print("Part 2:", len(paths2(pts - set(["start"]), False, ["start"])))
