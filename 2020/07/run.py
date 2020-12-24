from parse import parse

# Parse lines like "light red bags contain 1 bright white bag, 2 muted yellow bags."
#  => {'light red': {'bright white': 1, 'muted yellow': 2}, ... }
rules = [parse("{} bags contain {}.", d) for d in open("input.txt")]
rules = [[r[0], r[1].split(", ")] for r in rules]
rules = [[r[0], [parse("{:d} {} bag", rr) or parse("{:d} {} bags", rr) for rr in r[1]]] for r in rules]
rules = [[r[0], dict((rr[1], rr[0]) for rr in r[1] if rr)] for r in rules]
rules = dict(rules)

def can_hold_directly(holder, held):
    return held in rules[holder]

# breadth-first graph search -- just keep adding colors that can hold a color
# we've seen before until there are no more new ones
initial_pass = set(c for c in rules if can_hold_directly(c, "shiny gold"))
new = initial_pass
seen = initial_pass
while new:
    newer = set(c for c in rules if any(can_hold_directly(c, h) for h in new))
    newer = newer.difference(seen)
    seen = seen.union(newer)
    new = newer

print("Part 1:", len(seen))

def children(b):
    return sum(n + n*children(c) for (c,n) in rules[b].items())

print("Part 2:", children("shiny gold"))



