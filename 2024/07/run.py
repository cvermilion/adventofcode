from me import *

input = get_data_2024(7)

input = input_test

def parse_line(l):
	total, rest = l.strip().split(": ")
	nums = rest.split(" ")
	return int(total), lmap(int, nums)

lines = lmap(parse_line, input.splitlines())

# Part 1

def check(total, nums):
	if len(nums) == 1:
		return total == nums[0]
	if nums[0] > total:
		# none of the operators makes the total smaller
		return False
	return check(total, [nums[0]+nums[1]] + nums[2:]) or check(total, [nums[0]*nums[1]] + nums[2:])
	

result1 = sum(total for (total, nums) in lines if check(total, nums))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=7)

# Part 2

def check2(total, nums):
	if len(nums) == 1:
		return total == nums[0]
	if nums[0] > total:
		# none of the operators makes the total smaller
		return False
	return check2(total, [nums[0]+nums[1]] + nums[2:]) or check2(total, [nums[0]*nums[1]] + nums[2:]) or check2(total, [int(str(nums[0])+str(nums[1]))] + nums[2:])
	

result2 = sum(total for (total, nums) in lines if check2(total, nums))

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=7)
