from me import *

input = get_data_2023(4)

#input = input_test

# Part A

resultA = sum(pipe(
	input.splitlines(),
	lambda s: s.split(":")[1].split("|"),
	lambda sides: lpipe(sides, str.strip, [str.split, " "], partial(filter, len), partial(map, int), set),
	lambda sides: set.intersection(*sides),
	len,
	lambda n: 2**(n-1) if n else 0
	))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=4)

# Part B

matches = lpipe(
	input.splitlines(),
	lambda s: s.split(":")[1].split("|"),
	lambda sides: lpipe(sides, str.strip, [str.split, " "], partial(filter, len), partial(map, int), set),
	lambda sides: set.intersection(*sides),
	len
	)

copies = [1]*len(matches)
for i in range(len(copies)):
	for j in range(i+1, i+1+matches[i]):
		copies[j] += copies[i]

resultB = sum(copies)
print("Part B:", resultB)
aocd.submit(resultB, part="b", day=4)
