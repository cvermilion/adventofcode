from me import *
from sickos.yes import *

DAY=3

#input = get_data_2025(DAY)
input = input_test

banks = (pipeline(input.splitlines()) | [[int]] | DONE)

# max using n digits
def max_joltage(n, bank):
	if n == 0:
		return 0
	usable = bank[:-(n-1)] if n>1 else bank
	first = bank.index(max(usable))
	return bank[first]*10**(n-1) + max_joltage(n-1, bank[first+1:])

# Part 1

result1 = sum(max_joltage(2, b) for b in banks)
print("Part 1:", result1)
#aocd.submit(result1, part="a", day=DAY)

# Part 2

result2 = sum(max_joltage(12, b) for b in banks)
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=DAY)
