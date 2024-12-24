from me import *
from sickos.yes import *
from collections import deque
from functools import cmp_to_key
import string

input = get_data_2024(24)

input = input_test
input = open("input_test2.txt").read()

"""
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
"""

# Part 1

def toposort(gg):
	gg = deque(gg)
	out = []
	seen = set()
	while gg:
		g = gg.popleft()
		if (g["a"][0] in "xy" or g["a"] in seen) and (g["b"][0] in "xy" or g["b"] in seen):
			out.append(g)
			seen.add(g["c"])
		else:
			gg.append(g)
	return out

ops = {"AND": "&", "OR":"|", "XOR": "^" }

def gates_to_code(s):
	vals, gates = s.split("\n\n")
	vals = vals.replace(":", " =")
	
	gates = (pipeline(gates)
		| str.splitlines
		| [partial(parse, "{a} {op} {b} -> {c}")]
		| [lambda r: r.named | {"op": ops[r["op"]]}]
		| toposort
		| [lambda g: "{c} = {a} {op} {b}".format(**g)]
		| "\n".join
		| DONE
	)
	return vals + "\n" + gates

# YES... YES!
exec(gates_to_code(input))

digs = count(g for g in globals() if g.startswith("z"))
result1 = sum(eval("z{:02d}".format(i))<<i for i in range(digs))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=24)

# Part 2

result2 = None
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=24)