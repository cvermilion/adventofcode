from me import *
from sickos.yes import *
from operator import add, mul

DAY=6

input = get_data_2025(DAY)

input = input_test

# Part 1

lines = input.splitlines()
op_strs = filter(lambda x:x, lines.pop().split(" "))
ops = lmap(lambda o: {"+": add, "*": mul}[o], op_strs)

result1 = (pipeline(lines)
  | [(str.split, " ")]
  | [partial(filter, lambda x: x)]
  | [[int]]
  | transpose
  | (lambda cols: zip(cols, ops))
  | [lambda col, op: reduce(op, col)]
  | sum
  | DONE)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=DAY)

# Part 2
def split_on(l, val):
	while val in l:
		idx = l.index(val)
		yield l[:idx]
		l = l[idx+1:]
	yield l
	
result2 = (pipeline(lines)
	| transpose
	| ["".join]
	| [str.strip]
	| (split_on, "")
	| [[int]]
	| (lambda cols: zip(cols, ops))
	| [lambda col, op: reduce(op, col)]
	| sum
	| DONE)


print("Part 2:", result2)
#aocd.submit(result2, part="b", day=DAY)