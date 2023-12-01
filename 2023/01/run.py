import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#input = input_test
input = get_data(1)

# Part a

def is_dig(c):
	return c in '0123456789'

resultA = sum(thread(
	input.splitlines(),
	partial(filter, is_dig),
	partial(lmap, int),
	lambda dd: 10*dd[0]+dd[-1]
))
print("Part a:", resultA)
aocd.submit(resultA, part="a", day=1)

# part b

input_test = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
#input = input_test.strip()

digit_strings = {
	"one": 1,
	"two": 2,
	"three": 3,
	"four": 4,
	"five": 5,
	"six": 6,
	"seven": 7,
	"eight": 8,
	"nine": 9
}
p = re.compile("(?=(\d|" + "|".join(digit_strings.keys()) + "))")

def parse_int(s):
	return digit_strings.get(s) if s in digit_strings else int(s)
	
resultB = sum(thread(
	input.splitlines(),
	p.findall,
	partial(lmap, parse_int),
	lambda dd: 10*dd[0]+dd[-1]
))

print("Part b:", resultB)
aocd.submit(resultB, part="b", day=1)
