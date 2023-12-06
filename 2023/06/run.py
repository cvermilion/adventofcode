from me import *
from math import sqrt, floor, ceil

input = get_data_2023(6)

#input = input_test

# Part A

num_pat = re.compile("\d+")
nums = lmap(int, num_pat.findall(input))
tds = list(zip(nums[:len(nums)//2], nums[len(nums)//2:]))

# wait w secs
# dist = w*(t-w) = tw - w**2
# max: t - 2w = 0 => w = t/2
# problem is d > d0
# find sols and take range between
# w**2 - tw + d0 = 0

def range(td):
	t,d = td
	# this is symmetric around t/2 so we don't need both but honestly this feels
	# lazier than dealing with t/2 maybe being half-integer
	(low, high) = (.5*(t - sqrt(t**2 - 4*d)), .5*(t + sqrt(t**2 - 4*d)))
	rounded_low, rounded_high = ceil(low), floor(high)
	if rounded_low == low:
		rounded_low += 1
	if rounded_high == high:
		rounded_high -= 1
	return rounded_high - rounded_low + 1

resultA = product(map(range, tds))
print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=6)

# Part B

lines = input.splitlines()
t = int("".join(num_pat.findall(lines[0])))
d = int("".join(num_pat.findall(lines[1])))
resultB = range((t,d))
print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=6)
