from me import *
from sickos.yes import *
import re

input = get_data_2024(3)

#input = input_test

# Part 1

pat = re.compile(r"mul\(\d+,\d+\)")
result1 = (
	pipeline(pat.findall(input))
	| [partial(parse, "mul({:d},{:d})")]
	| [product] | sum | DONE
)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=3)

# Part 2

#input = open("input_test2.txt").read()

pat = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")

active = True
tot = 0
for s in pat.findall(input):
	if s == "do()":
		active = True
	elif s == "don't()":
		active = False
	elif active:
		a,b = parse("mul({:d},{:d})", s)
		tot += a*b

result2 = tot

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=3)
