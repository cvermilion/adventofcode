from me import *

input = get_data_2025(1)

#input = input_test

def parse_dir(s):
	# sickos.jpg
	return int(s[1:]) * int((ord(s[0])-79)/3)

# Part 1

steps = [parse_dir(l) for l in input.splitlines()]

clicks = 0
cur = 50
for s in steps:
	cur = (cur + s) % 100
	if cur == 0:
		clicks += 1

result1 = clicks

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=1)

# Part 2

clicks = 0
cur = 50
for s in steps:
	nxt = cur
	if s < 0 and cur != 0:
		# do a little jig so that |nxt+s|/100 is always the number of clicks
		nxt -= 100
	nxt += s
	clicks += int(abs(nxt)/100)
	cur = nxt%100

result2 = clicks
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=1)