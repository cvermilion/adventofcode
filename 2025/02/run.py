from me import *
from sickos.yes import *

input = get_data_2025(2)

input = input_test

# Part 1

ranges = (pipeline(input)
	| (str.split, ",")
	| [(str.split, "-")]
	| [[int]]
	| DONE)

def invalid_in_len_range(digs, x, y):
	if digs%2 == 1:
		return 0
	half_digs = int(digs/2)
	x_halves = (int(x / 10**half_digs), x % 10**half_digs)
	y_halves = (int(y / 10**half_digs), y % 10**half_digs)
	low_half = x_halves[0]
	if x_halves[0] < x_halves[1]:
		low_half += 1
	high_half = y_halves[0]
	if y_halves[0] > y_halves[1]:
		high_half -= 1
	low = low_half*(10**half_digs) + low_half
	high = high_half*(10**half_digs) + high_half
	sum = int((high_half - low_half + 1) * (high_half + low_half) / 2)
	return sum + sum*(10**half_digs)

def invalid_in_range(x,y):
	digs_x = len(str(x))
	digs_y = len(str(y))
	inv = 0
	if digs_x == digs_y:
		inv += invalid_in_len_range(digs_x, x, y)
	else:
		inv += invalid_in_len_range(digs_x, x, 10**digs_x - 1)
		digs = digs_x+1
		while digs < digs_y:
			inv += invalid_in_len_range(digs, 10**(digs-1), 10**digs - 1)
		inv += invalid_in_len_range(digs_y, 10**(digs_y-1), y)
	return inv
	

result1 = sum(invalid_in_range(x,y) for (x,y) in ranges)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=2)

# Part 2

def batch(iterable, n=1):
	l = len(iterable)
	for ndx in range(0, l, n):
		yield iterable[ndx:min(ndx + n, l)]

def sum_chunks(n, x):
	l = len(str(x))
	return x * sum(10**(i*l) for i in range(n))

# with n-digit chunks
def invalid_in_range_n(n, x, y):
	n_chunks = len(str(x))//n
	x_segs = lmap(int, batch(str(x), n))
	low_half = x_segs[0]
	if sum_chunks(n_chunks, low_half) < x:
		low_half += 1
	y_segs = lmap(int, batch(str(y), n))
	high_half = y_segs[0]
	if sum_chunks(n_chunks, high_half) > y:
		high_half -= 1
		
	if high_half < low_half:
		return 0

	res = int((high_half - low_half + 1) * (high_half + low_half) / 2)
	return res * sum(10**(i*n) for i in range(n_chunks))

def invalid_in_len_range(digs, x, y):
	# test and real data max out at 10-digit numbers
	# We have to consider all factors of digs,
	# but if A*B is a factor, we can skip A and B because A*B will cover them.
	# (Eg, 12121212 is covered by n=4, no need to check n=2.)
	# But note that adding multiple factors double-counts mutual factors, including 1. Up to 10 digits, we only have to consider 1 or 2 factors, and subtract the n=1 total in the latter case.
	lens = {
		1: [],
		4: [2],
		6: [2,3],
		8: [4],
		9: [3],
		10: [2,5],
	}.get(digs, [1])
	res = sum(invalid_in_range_n(n, x, y) for n in lens)
	if len(lens) == 2:
		# with multiple groupings we double count
		# eg, 222222
		res -= invalid_in_range_n(1, x, y)
	return res

def invalid_in_range(x,y):
	digs_x = len(str(x))
	digs_y = len(str(y))
	inv = 0
	if digs_x == digs_y:
		inv += invalid_in_len_range(digs_x, x, y)
	else:
		inv += invalid_in_len_range(digs_x, x, 10**digs_x - 1)
		digs = digs_x+1
		while digs < digs_y:
			inv += invalid_in_len_range(digs, 10**(digs-1), 10**digs - 1)
		inv += invalid_in_len_range(digs_y, 10**(digs_y-1), y)
	return inv
	

result2 = sum(invalid_in_range(x,y) for (x,y) in ranges)

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=2)