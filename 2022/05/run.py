import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

stack, moves = input.split("\n\n")

lines = stack.split("\n")
N = int(len(lines[-1])/4) + 1
H = len(lines)-1

# pad the lines to make this easier
lines = [l + " "*4*N for l in lines[:-1]]

cols = [[lines[H-1-i][4*c + 1] for i in range(H)] for c in range(N)]

stacks = [[c for c in col if c != " "] for col in cols]

moves = moves.splitlines()
moves = [parse("move {:d} from {:d} to {:d}", line) for line in moves]

for (count, frm, to) in moves:
	for _ in range(count):
		c = stacks[frm-1].pop()
		stacks[to-1].append(c)

print("Part 1:", "".join(s[-1] for s in stacks))

# reset for part 2
stacks = [[c for c in col if c != " "] for col in cols]

for (count, frm, to) in moves:
	stacks[frm-1], mv = stacks[frm-1][:-count], stacks[frm-1][-count:]
	stacks[to-1] += mv

print("Part 2:", "".join(s[-1] for s in stacks))
