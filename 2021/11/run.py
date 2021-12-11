data0 = """11111
19991
19191
19991
11111"""

data1 = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

data = """4871252763
8533428173
7182186813
2128441541
3722272272
8751683443
3135571153
5816321572
2651347271
7788154252"""

grid = [[int(c) for c in l] for l in data.split("\n")]
if len(grid) != len(grid[0]):
    print("grid not square!", len(grid), len(grid[0]))
    import sys
    sys.exit(1)

# borrowed a couple functions from 2020 day 17
def rep_grid(g):
    return "\n".join("".join("X" if el > 9 else str(el) for el in row) for row in g)

def nabes(N, i,j):
    nn = []
    if i > 0:
        nn.append([i-1, j])
        if j > 0:
            nn.append([i-1, j-1])
        if j < N-1:
            nn.append([i-1, j+1])
    if i < N-1:
        nn.append([i+1, j])
        if j > 0:
            nn.append([i+1, j-1])
        if j < N-1:
            nn.append([i+1, j+1])
    if j > 0:
        nn.append([i, j-1])
    if j < N-1:
        nn.append([i, j+1])
    return nn

def incr(g):
    for i in range(N):
        for j in range(N):
            g[j][i] += 1

N = len(grid)
pts = sum([[(i,j) for i in range(len(grid))] for j in range(len(grid))], [])
nn = dict(((i,j), nabes(N, i, j)) for (i,j) in pts)

def do_step(g):
    incr(g)
    seen_flashes = set([])
    next_flashes = set([(i,j) for (i,j) in pts if g[j][i] > 9])
    while next_flashes:
        seen_flashes |= next_flashes
        all_nabes = sum([nn[(i,j)] for (i,j) in next_flashes], [])
        for (i,j) in all_nabes:
            g[j][i] += 1
        next_flashes = set([(i,j) for (i,j) in pts if g[j][i] > 9]).difference(seen_flashes)
    for (i,j) in seen_flashes:
        g[j][i] = 0
    return len(seen_flashes)

total = 0
for i in range(100):
    total += do_step(grid)
print("Part 1:", total)


# part 2
grid = [[int(c) for c in l] for l in data.split("\n")]
step = 0
while True:
    do_step(grid)
    step += 1
    if sum(sum(grid, [])) == 0:
        print("Part 2:", step)
        break
