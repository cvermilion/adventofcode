import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

def parse_op(op_a, op, op_b):
	f = (lambda x,y: x+y) if op == "+" else (lambda x,y: x*y)
	if op_a == "old" and op_b != "old":
		b = int(op_b)
		return lambda x: f(x, b)
	elif op_a != "old" and op_b == "old":
		a = int(op_a)
		return lambda x: f(x, a)
	else:
		return lambda x: f(x, x)

def parse_monkey(s):
	lines = s.splitlines()
	#  Starting items: 79, 98
	items = [int(n) for n in lines[1][len("  Starting items: "):].split(", ")]
	#  Operation: new = old * 19
	op_a, op, op_b = parse("  Operation: new = {} {} {}", lines[2])
	#  Test: divisible by 23
	div = int(lines[3][len("  Test: divisible by "):])
	#    If true: throw to monkey 2
	true_case = int(lines[4][len("    If true: throw to monkey "):])
	false_case = int(lines[5][len("    If false: throw to monkey "):])
	return {
		"items": items,
		"op": parse_op(op_a, op, op_b),
		"div": div,
		"true": true_case,
		"false": false_case,
		"count": 0,
	}

monkeys = [parse_monkey(s) for s in input.split("\n\n")]

prod = reduce(operator.mul, (m["div"] for m in monkeys), 1)

def step(part1):
	for monkey in monkeys:
		while monkey["items"]:
			item, monkey["items"] = monkey["items"][0], monkey["items"][1:]
			new = monkey["op"](item)
			if part1:
				new = new // 3
			# Trick for part 2 (but safe for both):
			# Can keep just (new % N) where N is the
			# product of all the numbers we test
			# against in the last step.
			new = new % prod
			if new % monkey["div"] == 0:
				monkeys[monkey["true"]]["items"].append(new)
			else:
				monkeys[monkey["false"]]["items"].append(new)
			monkey["count"] = monkey["count"] + 1

for i in range(20):
	step(True)

counts = sorted(m["count"] for m in monkeys)
print("Part 1:", counts[-1] * counts[-2])

monkeys = [parse_monkey(s) for s in input.split("\n\n")]

for i in range(10000):
	step(False)

counts = sorted(m["count"] for m in monkeys)
print("Part 2:", counts[-1] * counts[-2])
