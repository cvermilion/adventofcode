input_test = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

from parse import parse

#input = input_test
input = open("input.py").read()

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

print("".join(s[-1] for s in stacks))

# reset for part 2
stacks = [[c for c in col if c != " "] for col in cols]

for (count, frm, to) in moves:
	stacks[frm-1], mv = stacks[frm-1][:-count], stacks[frm-1][-count:]
	stacks[to-1] += mv

print("".join(s[-1] for s in stacks))
