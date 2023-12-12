from me import *
from sickos.yes import *
from itertools import *

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
	"""How many ways can we allocate runs of damaged springs (#) into segments (sequences of springs that may be ./#/?)"""
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
	if sum(lens) + (len(segments)-1) < sum(runs)+(len(runs)-1) or max(lens) < max(runs):
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
	
	# divide and conquer over individual segments
	if len(segments) > 1:
		total = 0
		for i in range(len(runs)+1):
			left = nsols(segments[:1], runs[:i])
			if left:
				right = nsols(segments[1:], runs[i:])
				total += left*right
		return total
	
	# single segment, all unknown: simple analytic answer
	seg0 = segments[0]
	if len(segments) == 1 and seg0.count("#") == 0:
		return math.comb(len(seg0)-sum(runs)+1, len(runs))
		
	# one segment, but mix of # and ?: split on the last ? in the first block of ?'s
	# (that peels off as big a run of ?'s as we can for the first segment since we
	# can do that part analytically)
	split = seg0.find("#")
	split = seg0.find("?") if split <= 0 else split-1
	segs = [seg0[:split], seg0[split+1:]]
	
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
