from me import *
from sickos.yes import *

input = get_data_2023(5)

#input = input_test

# Part A

def do_map(ranges, src):
	for (start, end), shift in ranges:
		if src >= start and src < end:
			return src + shift
	return src

def parse_mapping(s):
	ranges = (pipeline(s)
		| str.strip
		| str.splitlines
		| (lambda lines: lines[1:])
		| [(str.split, " ")]
		| [[int]]
		# take [dst, src, span] and return ((src_start, src_end), offset) where offset is (dst-src)
		| [lambda l: ((l[1], l[1]+l[2]), l[0]-l[1])]
		| DONE)
	return partial(do_map, ranges)

blocks = input.split("\n\n")
seeds, maps = blocks[0], blocks[1:]

seeds = lmap(int, seeds.split(": ")[1].split(" "))
maps = lmap(parse_mapping, maps)

def do_maps(maps, seed):
	res = seed
	for m in maps:
		res = m(res)
	return res

resultA = min(do_maps(maps, s) for s in seeds)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=5)

# Part B

# Brute force version: this takes 90M to run 1.7B seeds on my M1 Max laptop.

seeds = [(seeds[2*i], seeds[2*i+1]) for i in range(len(seeds)//2)]

total = sum(s[1] for s in seeds)

best = do_maps(maps, seeds[0][0])
n = 1
for (start, run) in seeds:
	for seed in range(start, start+run):
		loc = do_maps(maps, seed)
		if loc < best:
			best = loc
		n+=1
		if n % 1000000 == 0:
			print("{} ({})".format(n, n/total))

resultB = best
print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=5)
