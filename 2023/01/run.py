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
	list,
	lambda dd: int(dd[0] + dd[-1])
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

def backward(s):
	return "".join(reversed(s))

digit_words = {
	"one": "1",
	"two": "2",
	"three": "3",
	"four": "4",
	"five": "5",
	"six": "6",
	"seven": "7",
	"eight": "8",
	"nine": "9"
}
# first match
pf = re.compile("\d|" + "|".join(digit_words.keys()))
# first match on a reversed string
pr = re.compile("\d|" + "|".join(map(backward, digit_words.keys())))

resultB = sum(thread(
	input.splitlines(),
	# [first_match, last_match]
	lambda s: [pf.search(s).group(0), backward(pr.search(backward(s)).group(0))],
	partial(lmap, lambda s: digit_words.get(s, s)),
	lambda dd: int(dd[0] + dd[-1])
))

print("Part b:", resultB)
aocd.submit(resultB, part="b", day=1)
