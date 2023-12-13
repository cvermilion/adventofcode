from me import *
from sickos.yes import *

input = get_data_2023(13)

input = input_test

def rep_grid(g):
	return "\n".join(g)

# Part A

def sum_diff_ref(g, i):
	"""Sum the differences across a reflection over column i"""
	size = min(i, len(g[0])-i)
	return sum(1 if row[i-n-1] != row[i+n] else 0 for n in range(size) for row in g)

def col_sum(g, ndiff):
	"""Sum the columns i where sum_diff_ref(g, i) == ndiff"""
	return sum(i for i in range(1,len(g[0])) if sum_diff_ref(g,i) == ndiff)

def do_sums(ndiff):
	"""ndiff=0 for a match, ndiff=1 for off-by-one"""
	return (
		pipeline(input.split("\n\n"))
		| [str.splitlines]
		| [[list]]
		| [lambda g: 100*col_sum(list(zip(*g)), ndiff) + col_sum(g, ndiff)]
		| sum
		| DONE
	)

resultA = do_sums(0)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=13)

# Part B

resultB = do_sums(1)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=13)
