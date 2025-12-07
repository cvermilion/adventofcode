from me import *
DAY=7
input = get_data_2025(DAY)
input = input_test

# Part 1

lines = input.splitlines()
init_row, lines = lines[0], lines[1:]
beams = [init_row.index("S")]
splits = 0
for line in lines:
	nxt_beams = set()
	for beam in beams:
		if line[beam] == "^":
			nxt_beams.add(beam-1)
			nxt_beams.add(beam+1)
			splits += 1
		else:
			nxt_beams.add(beam)
	beams = nxt_beams

result1 = splits

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=DAY)

# Part 2

paths_to = {init_row.index("S"): 1}
for line in lines:
	nxt_paths = {}
	for beam, n in paths_to.items():
		if line[beam] == "^":
			nxt_paths[beam-1] = nxt_paths.get(beam-1,0) + n
			nxt_paths[beam+1] = nxt_paths.get(beam+1,0) + n
		else:
			nxt_paths[beam] = nxt_paths.get(beam,0) + n
	paths_to = nxt_paths
	
result2 = sum(nxt_paths.values())
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=DAY)