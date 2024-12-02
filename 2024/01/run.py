from me import *

input = get_data_2024(1)

#input = input_test

# Part 1

def absdiff(pair):
	return abs(pair[0] - pair[1])

pairs = lmap(partial(parse, "{:d}  {:d}"), input.splitlines())

lists = transpose(pairs)
sorted_pairs = zip(*map(sorted, lists))

result1 = sum(lmap(absdiff, sorted_pairs))

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=1)

# Part 2

l0, l1 = lists
result2 = sum(n*l1.count(n) for n in l0)

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=1)
