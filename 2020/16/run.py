from functools import reduce
from operator import mul
from parse import parse

rules = [parse("{}: {:d}-{:d} or {:d}-{:d}", l) for l in open("rules.txt")]
rules = dict((r[0], [[r[1],r[2]],[r[3],r[4]]]) for r in rules)

tickets = [[int(s) for s in l.split(",")] for l in open("tickets.txt")]

all_values = {}
for r in rules.values():
    for rr in r:
        for i in range(rr[0], rr[1]+1):
            all_values[i] = True

invalid_total = 0
for t in tickets:
    for x in t:
        if not x in all_values:
            invalid_total += x

print("Part 1:", invalid_total)

#my_ticket = [11,12,13]
my_ticket = [101,179,193,103,53,89,181,139,137,97,61,71,197,59,67,173,199,211,191,131]

valid_tickets = []
for t in tickets:
    if not any(x not in all_values for x in t):
        valid_tickets.append(t)

vals_by_index = dict((i, set(t[i] for t in valid_tickets)) for i in range(len(tickets[0])))

possible_rules = dict((i, set()) for i in range(len(tickets[0])))
for i in range(len(tickets[0])):
    for name,r in rules.items():
        check = lambda x: (x >= r[0][0] and x <= r[0][1]) or (x >= r[1][0] and x <= r[1][1])
        if all(check(x) for x in vals_by_index[i]):
            possible_rules[i].add(name)

known_rules = {}
while possible_rules:
    next_pass = dict((i,names) for (i,names) in possible_rules.items() if len(names) == 1)
    for i,names in next_pass.items():
        name = names.pop()
        known_rules[i] = name
        del possible_rules[i]
        for i, names in possible_rules.items():
            names.remove(name)

departure_fields = [i for (i, name) in known_rules.items() if name.startswith("departure")]
print("Part 2:", reduce(mul, (my_ticket[i] for i in departure_fields)))
