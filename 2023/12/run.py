from me import *
from sickos.yes import *

input = get_data_2023(12)

input = input_test

# Part A

springs = (pipeline(input.splitlines())
	| [(str.split, " ")]
	| [lambda s, nn: (s, lmap(int, nn.split(",")))]
	| [lambda s, nn: (list(filter(len, s.split("."))), nn)]
	| DONE
	)

def nsols(segments, runs):
	"""How many ways can we allocate runs of damaged springs (#) into segments (sequences of springs that are either '#' or '?')?"""
	if not segments:
		# Nowhere left to put anything
		return 0 if runs else 1
	if len(segments[0]) == 0:
		# ignore empty segments
		return nsols(segments[1:], runs)
	min_broken = sum(s.count("#") for s in segments)
	if not runs:
		return 1 if min_broken == 0 else 0
	lens = lmap(len, segments)
	if sum(lens) < sum(runs) or max(lens) < max(runs):
		# No solutions: not enough possibly broken springs, or no segment long enough for longest run
		return 0
	# Consume known runs on either end
	if segments[0].count("?") == 0:
		if len(segments[0]) != runs[0]:
			return 0
		else:
			return nsols(segments[1:], runs[1:])
	if segments[-1].count("?") == 0:
		if len(segments[-1]) != runs[-1]:
			return 0
		else:
			return nsols(segments[:-1], runs[:-1])
	
	# Better solve here: divide and conquer over individual segments
	
	# For now, naive solve: take first ? and sum solutions for both possibilities
	
	# First segment must have a ?, we handled other case
	segs = segments[0].split("?", 1)
	assert(len(segs) == 2)
	# working case: this splits first segment in two
	working = nsols(segs + segments[1:], runs)
	broken = nsols(["#".join(segs)]+segments[1:], runs)
	return working+broken

resultA = sum(nsols(segs, runs) for (segs, runs) in springs)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=12)

# Part B

springs = (pipeline(input.splitlines())
	| [(str.split, " ")]
	| [lambda s, nn: (s, lmap(int, nn.split(",")))]
	| [lambda s, nn: ("?".join(5*[s]), 5*nn)]
	| [lambda s, nn: (list(filter(len, s.split("."))), nn)]
	| DONE
	)

resultB = sum(nsols(segs, runs) for (segs, runs) in springs)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=12)
