from me import *

input = get_data_2023(15)
#input = input_test

# Part A

def hash_(s):
	h = 0
	for c in s:
		h = ((h+ord(c))*17)%256
	return h

steps = input.strip().split(",")
resultA = sum(hash_(s) for s in steps)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=15)

# Part B

# NB: Python dicts are ordered now, for great justice

boxes = [{} for i in range(256)]
for step in steps:
	if "-" in step:
		label = step[:-1]
		h = hash_(label)
		if label in boxes[h]:
			del boxes[h][label]
	else:
		label, val = step.split("=")
		h = hash_(label)
		boxes[h][label] = int(val)

resultB = sum(
	(b+1)*sum((i+1)*val for (i,val) in enumerate(box.values()))
	for (b,box) in enumerate(boxes)
)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=15)
