import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

# model two instructions as int or None

instrs = [l.strip() for l in input.splitlines()]
instrs = [None if l == "noop" else int(l[5:]) for l in instrs]

# part 1
cycle = 0
x = 1
strength = 0
# part 2
screen = [["." for i in range(40)] for j in range(6)]

def draw():
	global strength
	# part 1
	if (cycle - 20) % 40 == 0:
		strength += x*cycle
	# part 2
	row, pixel = cycle // 40, ((cycle-1) % 40)
	if abs(pixel - x) <= 1:
		screen[row][pixel] = "#"
		

for instr in instrs:
	if instr is None:
		cycle += 1
		draw()
	else:
		cycle += 1
		draw()
		cycle += 1
		draw()
		x += instr

print("Part 1:", strength)

print("Part 2:")
for row in screen:
	print("".join(row))
