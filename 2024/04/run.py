from me import *

input = get_data_2024(4)

input = input_test

# Part 1

grid = lmap(list, input.strip().split("\n"))

def rep_grid(g):
    return "\n".join("".join(row) for row in g)

def padded(N, c, grid):
	gx = len(grid[0])
	return (
		[[c] * (gx+2*N)] * N
		+ [[c]*N + row + [c]*N for row in grid]
		+ [[c] * (gx+2*N)] * N
	)

Ni = len(grid[0])
Nj = len(grid)
grid = padded(3, ".", grid)
#print(rep_grid(padded(1, ".", grid)))

tot = 0
MAS = list("MAS")
SAM = list("SAM")
for j in range(3, Nj+3):
	for i in range(3, Ni+3):
		if grid[j][i] == "X":
			# right
			if grid[j][i+1:i+4] == MAS:
				tot += 1
			# left
			if grid[j][i-3:i] == SAM:
				tot += 1
			# down
			if [grid[j+n][i] for n in range(1,4)] == MAS:
				tot += 1
			# up
			if [grid[j-n][i] for n in range(1,4)] == MAS:
				tot += 1
			# up-right
			if [grid[j-n][i+n] for n in range(1,4)] == MAS:
				tot += 1
			# down-right
			if [grid[j+n][i+n] for n in range(1,4)] == MAS:
				tot += 1
			# down-left
			if [grid[j+n][i-n] for n in range(1,4)] == MAS:
				tot += 1
			# up-left
			if [grid[j-n][i-n] for n in range(1,4)] == MAS:
				tot += 1

result1 = tot

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=4)

# Part 2

SnM = set("SM")
tot = 0

for j in range(3, Nj+3):
	for i in range(3, Ni+3):
		if grid[j][i] == "A":
			if set([grid[j-1][i-1], grid[j+1][i+1]]) == SnM and set([grid[j-1][i+1], grid[j+1][i-1]]) == SnM:
				tot += 1

result2 = tot
print("Part 2:", result2)
#aocd.submit(result2, part="b", day=4)
