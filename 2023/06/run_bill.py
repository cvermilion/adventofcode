from me import *
from sickos.yes import *

# adapted from Bill's version: https://notes.billmill.org/programming/advent_of_code/2023_problem_log.html#day-6

input = get_data_2023(6)

#input = input_test

# Part A

resultA = (
	pipeline(input.splitlines())
	| [partial(re.findall, r"\d+")]
	| [[int]]
	| splat(zip)
	| [lambda t, d: sum(1 for p in range(t) if (t-p)*p > d)]
	| product
	| DONE
)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=6)

# Part B

resultB = (
	pipeline(input.splitlines())
	| [partial(re.findall, r"\d+")]
	| ["".join]
	| [int]
	| (lambda t, d: sum(1 for p in range(t) if (t-p)*p > d))
	| DONE
)
print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=6)
