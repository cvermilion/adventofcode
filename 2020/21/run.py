data = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

data = open("input.py").read()

from parse import parse
from functools import reduce
import operator

def parse_line(s):
	allergens = []
	if "(" in s:
		r = parse("{} (contains {})", s)
		ings = r[0].split(" ")
		allergens = r[1].split(", ")
	else:
		ings = s.split(" ")
	return set(ings), set(allergens)

foods = list(map(parse_line, data.splitlines()))

all_allergens = reduce(set.union, [f[1] for f in foods])
possibilities = dict((a, reduce(set.intersection, [f[0] for f in foods if a in f[1]])) for a in all_allergens)

container = {}
while possibilities:
	known = set(container.keys())
	possibilities = dict((a, f.difference(known)) for (a,f) in possibilities.items())
	
	to_remove = []
	for a, ff in possibilities.items():
		if len(ff) == 1:
			f = ff.pop()
			container[f] = a
			to_remove.append(a)
	for a in to_remove:
		del possibilities[a]

# now find foods with no allergens
clear = []
for ff, aa in foods:
	for f in ff:
		if f not in container:
			clear.append(f) # include duplicates because we want a count

print("Part 1:", len(clear))

atof = dict((a,f) for (f,a) in container.items())
sor = sorted(atof.keys())
print("Part 2:", ",".join(atof[a] for a in sor))


