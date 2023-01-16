import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

dig_map = {"0":0, "1":1, "2": 2, "-": -1, "=": -2}

def d(c):
	return dig_map[c]

def c(d):
	m = dict((v,k) for (k,v) in dig_map.items())
	return m[d]
	
def parse_num(n):
	digs = [d(c) for c in n]
	return sum(x*(5**i) for (i,x) in enumerate(reversed(digs)))

# base5 digits in increasing order
def base_five_digs(n):
	res = []
	while n:
		x = n % 5
		n = n // 5
		res.append(x)
	while res[-1] == 0:
		res = res[:-1]
	return res

# snafu digits in increasing order
def snafu(b5_digs):
	sdigs = [0]* (len(b5_digs)+1)
	for (i, d) in enumerate(b5_digs):
		sdigs[i] += d
		if sdigs[i] > 2:
			sdigs[i+1] = 1
			sdigs[i] = sdigs[i] - 5
	while sdigs[-1] == 0:
		sdigs = sdigs[:-1]
	return sdigs

def snafu_str(digs):
	return "".join(reversed(list(map(c, digs))))

nums = [parse_num(l) for l in input.splitlines()]

print("Part 1:", snafu_str(snafu(base_five_digs(sum(nums)))))
