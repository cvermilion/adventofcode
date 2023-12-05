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

# returns a list of mappings for each stage
# a single map looks like ((start, end), offset), specifying that [start, end) is mapped to [start+offset, end+offset) by that map
def parse_maps(s):
	return (pipeline(s)
		| str.strip
		| str.splitlines
		| (lambda lines: lines[1:])
		| [(str.split, " ")]
		| [[int]]
		| [lambda l: ((l[1], l[1]+l[2]), l[0]-l[1])]
		| DONE)
	
# Merge one map with the next stage's maps
def merge_maps(m1, mm2):
	mm2 = sorted(mm2)
	(src1_start, src1_end), offset1 = m1
	(dest1_start, dest1_end) = (src1_start+offset1, src1_end+offset1)
	merged = []
	# Scan through the intersections of m1's dest range and next stage's source ranges.
	for m2 in mm2:
		(src2_start, src2_end), offset2 = m2
		if dest1_start < src2_start:
			# At least some of this map's destination range isn't covered by
			# m2's source; extract that part.  It just passes through with the
			# current offset.
			span = min([src2_start, dest1_end]) - dest1_start
			merged.append(((src1_start, src1_start+span), offset1))
			
			src1_start += span
			dest1_start += span
			if src1_start == src1_end:
				# All done!
				break
		if dest1_start < src2_end:
			# Full or partial overlap with m2.
			if dest1_end <= src2_end:
				# Total overlap.
				merged.append(((src1_start, src1_end), offset1+offset2))
				src1_start = src1_end
				dest1_start = dest1_end
				if src1_start == src1_end:
					# All done!
					break
			else:
				# Partial overlap, extract overlap part.
				span = src2_end - dest1_start
				merged.append(((src1_start, src1_start+span), offset1+offset2))
				src1_start += span
				dest1_start = src1_start + offset1
	# if we get here, there is dest1 range left not covered by any mm2 source
	if src1_start < src1_end:
		merged.append(((src1_start, src1_end), offset1))
	return merged

# initial seeds: (start, span) pairs
seeds = [(seeds[2*i], seeds[2*i+1]) for i in range(len(seeds)//2)]
mappings = lmap(parse_maps, map_chunks)

# Now, start with the initial seed ranges and iteratively merge with the
# mappings for the next stage.  Express the initial step as ((start, end), 0)
# mappings, and then the final result is a list of mappings from the initial
# seed ranges to their final locations.
flattened = [((s[0], s[0]+s[1]), 0) for s in seeds]
for mapping in mappings:
	flattened = sum((merge_maps(m, mapping) for m in flattened), [])

# For each mapping in the final list, its lowest location is just its first element plus the offset.
resultB = min(r[0][0]+r[1] for r in flattened)
print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=5)
