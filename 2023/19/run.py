from me import *
from collections import namedtuple
from copy import deepcopy

input = get_data_2023(19)

#input = input_test

# Part A

# this seemed like a good idea at the time
Part = namedtuple("Part", ["x", "m", "a", "s"])

stepsStr, partsStr = lmap(str.splitlines, input.split("\n\n"))

def parse_rule(s):
	if not ":" in s:
		return (lambda p: True, s)
	cond, dest = s.split(":")
	op = "<" if "<" in cond else ">"
	cat, val = cond.split(op)
	val = int(val)
	if op == "<":
		# oh god oh no
		return (lambda p: eval("p."+cat) < val, dest)
	else:
		return (lambda p: eval("p."+cat) > val, dest)

# px{a<2006:qkq,m>2090:A,rfg}
def parse_step(l):
	name, rules = l[:-1].split("{")
	rules = lmap(parse_rule, rules.split(","))
	return name, rules

# {x=787,m=2655,a=1222,s=2876}
def parse_part(l):
	# lol. lmao.
	return Part(*lmap(int, re.findall(r"\d+", l)))

steps = dict(parse_step(s) for s in stepsStr)
parts = lmap(parse_part, partsStr)

def accepted(p):
	cur = "in"
	while cur not in ["A", "R"]:
		rules = steps[cur]
		for (check, nxt) in rules:
			if check(p):
				cur = nxt
				break
	return cur == "A"

resultA = sum(sum(p) for p in parts if accepted(p))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=19)

# Part B

# range: map of xmas chars to [low, high) range tuples
start = dict((c, (1,4001)) for c in "xmas")

# returns (pass, fail) ranges
def split_range(cat, op, val, rng):
	low,high = rng[cat]
	if op == "<":
		if high <= val:
			return (rng, None)
		if val <= low:
			return (None, rng)
		l = deepcopy(rng)
		l[cat] = low, val
		r = deepcopy(rng)
		r[cat] = val, high
		return (l, r)
	else:
		if low > val:
			return (rng, None)
		if val >= high-1:
			return (None, rng)
		l = deepcopy(rng)
		l[cat] = low, val+1
		r = deepcopy(rng)
		r[cat] = val+1, high
		return (r, l)
 
def parse_rule(s):
	if not ":" in s:
		return (lambda r: (r,None), s)
	cond, dest = s.split(":")
	op = "<" if "<" in cond else ">"
	cat, val = cond.split(op)
	val = int(val)
	return (lambda r: split_range(cat, op, val, r), dest)

steps = dict(parse_step(s) for s in stepsStr)

accept = []
to_check = [(start, "in")]
while to_check:
	r, cur = to_check.pop()
	if cur == "A":
		accept.append(r)
		continue
	if cur == "R":
		continue
	for (chk, nxt) in steps[cur]:
		pass_, fail = chk(r)
		assert(pass_ or fail)
		if pass_:
			to_check.append((pass_, nxt))
		if fail:
			r = fail
		else:
			break

def score(r):
	return product(h-l for (l,h) in r.values())
		
resultB = sum(score(r) for r in accept)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=19)
