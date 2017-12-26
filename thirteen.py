# hit if t % (2r-1) == 0, t=d+1 (r = range, d is depth)

text="""0: 5
1: 2
2: 3
4: 4
6: 6
8: 4
10: 8
12: 6
14: 6
16: 8
18: 6
20: 9
22: 8
24: 10
26: 8
28: 8
30: 12
32: 8
34: 12
36: 10
38: 12
40: 12
42: 12
44: 12
46: 12
48: 14
50: 12
52: 14
54: 12
56: 14
58: 12
60: 14
62: 14
64: 14
66: 14
68: 14
70: 14
72: 14
76: 14
80: 18
84: 14
90: 18
92: 17"""

layers = [l.split(": ") for l in text.splitlines()]
layers = [(int(l[0]), int(l[1])) for l in layers]

layers = dict(layers)
print(layers)

def score(delay):
	any_hit = False
	score = 0
	for depth, range in layers.items():
		hit = (depth + delay) % (2*range - 2) == 0
		if hit:
			any_hit = True
			score += depth*range
	return any_hit, score

print(score(0))

delay=0
while True:
	if not score(delay)[0]:
		break
	delay+=1
print(delay)
