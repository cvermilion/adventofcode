from me import *
from sickos.yes import *
from collections import deque
from functools import cmp_to_key
import string

input = get_data_2024(24)

#input = input_test
#input = open("input_test2.txt").read()

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

# ok, FINE

def parse_gates(s):
	vals, gates = s.split("\n\n")
	vals = (pipeline(vals)
		| str.splitlines
		| [(str.split, ": ")]
		| [lambda s,n: (s, int(n))]
		| dict
		| DONE
	)
	
	gates = (pipeline(gates)
		| str.splitlines
		| [partial(parse, "{a} {op} {b} -> {c}")]
		| [lambda r: (r["c"], (r["op"], (r["a"], r["b"])))]
		| dict
		| DONE
	)
	return vals, gates

vals, gates = parse_gates(input)

# inspecting the real input shows the setup is
# just a directly implemented binary adder with
# some swaps, so I just worked out the pattern
# and looked for the ones that were different

# z_i = (x_i ^ y_i) ^ carry_i
# carry_(i+1) = (carry_i & (x_i ^ y_i)) | (x_i & y_i)

# x_i ^ y_i gates
bit_xors = [None] * (digs-1)
for g, (op, (a,b)) in gates.items():
	a,b = sorted((a,b))
	if op == "XOR" and a.startswith("x") and b.startswith("y") and a[1:] == b[1:]:
		bit_xors[int(a[1:])] = g

bit_xor_map = dict((g,i) for (i,g) in enumerate(bit_xors))

# x_i & y_i
bit_ands = [None] * (digs-1)
for g, (op, (a,b)) in gates.items():
	a,b = sorted((a,b))
	if op == "AND" and a.startswith("x") and b.startswith("y") and a[1:] == b[1:]:
		bit_ands[int(a[1:])] = g

bit_and_map = dict((g,i) for (i,g) in enumerate(bit_ands))

# carry_i
carries = [None] * digs
# cross-check: carry_i ^ (x_i ^ y_i) terms,
# should be z_i
carry_xors = [None] * digs
for g, (op, (a,b)) in gates.items():
	a,b = sorted((a,b))
	if op == "XOR" and a in bit_xor_map:
		idx = bit_xor_map[a]
		carry_xors[idx] = g
		carries[idx] = b
	elif op == "XOR" and b in bit_xor_map:
		idx = bit_xor_map[b]
		carry_xors[idx] = g
		carries[idx] = a

# z06 is actually (x6 & y6)
# z31 is OR xor_31 (AND xor_31 carry_30)
# z37 is AND xor_37 (OR bit_and_36 (AND xor_36 (OR bit_and_35 (AND xor_35 (OR )))))
# z45 is OR (AND xor_44 .. ) (bit_and_44)

# z06 is bit_and_6 -> swap with hwk
# so z31 is carry_32 -> swap with hpc
# z37 is LHS OF carry_38 -> swap with cgr

# z45 is carry_45 (ok!)

# carry_25 missing
# carry_32 wrong -- see z31 above

# z26 = XOR xor_26 khj
# z25 = XOR bit_and_25 carry_25
# khj = OR xor_25 (AND bit_and_25 (OR bit_and_24 (AND ..))) => nbs is carry_25

# tnt=bit_and_25 swap with xor_25=qmd

swaps = ",".join(sorted(["z06", "hwk", "z31", "hpc", "z37", "cgr", "tnt", "qmd"]))

result2 = swaps
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=24)