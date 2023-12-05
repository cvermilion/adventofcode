from me import *
from sickos.yes import *

input = get_data_2023(5)

input = input_test

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
		| [lambda l: ((l[1], l[1]+l[2]), l[0]-l[1])]
		| DONE)
	return partial(do_map, ranges)

chunks = input.split("\n\n")
seeds, map_chunks = chunks[0], chunks[1:]

seeds = lmap(int, seeds.split(": ")[1].split(" "))
maps = lmap(parse_mapping, map_chunks)

def all_maps(maps, seed):
	res = seed
	for m in maps:
		res = m(res)
	return res

resultA = min(map(partial(all_maps, maps), seeds))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=5)

# Part B

def parse_ranges(s):
	ranges = (pipeline(s)
		| str.strip
		| str.splitlines
		| (lambda lines: lines[1:])
		| [(str.split, " ")]
		| [[int]]
		| [lambda l: ((l[1], l[1]+l[2]), l[0]-l[1])]
		| DONE)
	return ranges
	
# Merge one map with the next stage's maps
def merge_maps(m1, mm2):
	mm2 = sorted(mm2)
	(src1_start, src1_end), offset1 = m1
	(dest1_start, dest1_end) = (src1_start+offset1, src1_end+offset1)
	merged = []
	# scan through the intersections of m1's dest range and next stage's source ranges
	for m2 in mm2:
		if src1_start == src1_end:
			# all done!
			break
		(src2_start, src2_end), offset2 = m2
		if dest1_start < src2_start:
			# this chunk of the first range just passes through, it doesn't match a source range in mm2
			span = min([src2_start - dest1_start, dest1_end - dest1_start])
			merged.append(((src1_start, src1_start+span), offset1))
			
			src1_start += span
			dest1_start += span
		if src1_start == src1_end:
			# all done!
			break
		if dest1_start < src2_end:
			# full or partial overlap
			if dest1_end <= src2_end:
				# total overlap
				merged.append(((src1_start, src1_end), offset1+offset2))
				src1_start = src1_end
				dest1_start = dest1_end
			else:
				# partial overlap, extract overlap part
				span = src2_end - dest1_start
				merged.append(((src1_start, src1_start+span), offset1+offset2))
				src1_start += span
				dest1_start = src1_start + offset1
	# if we get here, there is dest1 range left not covered by any mm2 source
	if src1_start < src1_end:
		merged.append(((src1_start, src1_end), offset1))
	return merged

seeds = [(seeds[2*i], seeds[2*i+1]) for i in range(len(seeds)//2)]
ranges = lmap(parse_ranges, map_chunks)

flattened = [((s[0], s[0]+s[1]), 0) for s in seeds]
for stage in ranges:
	flattened = sum((merge_maps(m, stage) for m in flattened), [])

resultB = min(r[0][0]+r[1] for r in flattened)
print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=5)
