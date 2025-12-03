from me import *
from sickos.yes import *

DAY=3

input = get_data_2025(DAY)

input = input_test

# Part 1

banks = (pipeline(input.splitlines())
	| [[int]]
	| DONE)

def max_joltage(bank):
	first = bank.index(max(bank[:-1]))
	second = first + 1 + bank[first+1:].index(max(bank[first+1:]))
	return 10*bank[first] + bank[second]


result1 = sum(map(max_joltage, banks))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=DAY)

# Part 2

# max using n digits
def max_joltage(n, bank):
	if n == 0:
		return 0
	usable = bank[:-(n-1)] if n>1 else bank
	first = bank.index(max(usable))
	return bank[first]*10**(n-1) + max_joltage(n-1, bank[first+1:])

result2 = sum(max_joltage(12, b) for b in banks)

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=DAY)
