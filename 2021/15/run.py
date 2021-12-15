data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

data = open("input.txt").read()

grid = [[int(c) for c in l] for l in data.split("\n") if l]
if len(grid) != len(grid[0]):
    print("grid not square!", len(grid), len(grid[0]))
    import sys
    sys.exit(1)
N = len(grid)

# borrowed a couple functions from 2020 day 17
def rep_grid(g):
    return "\n".join("".join("X" if el > 9 else str(el) for el in row) for row in g)

def nabes(N,i,j):
    nn = []
    if i > 0:
        nn.append([i-1, j])
    if i < N-1:
        nn.append([i+1, j])
    if j > 0:
        nn.append([i, j-1])
    if j < N-1:
        nn.append([i, j+1])
    return nn

def find_cost(grid):
    N = len(grid)
    costs = [[None for i in range(N)] for j in range(N)]
    costs[0][0] = 0
    nxt = [(0,0)]
    while nxt:
        cur, nxt = nxt[0], nxt[1:]
        cur_cost = costs[cur[1]][cur[0]]
        for (i,j) in nabes(N, *cur):
            cost = cur_cost + grid[j][i]
            if costs[j][i] is None or cost < costs[j][i]:
                costs[j][i] = cost
                nxt.append((i,j))
    return costs[N-1][N-1]

print("Part 1:", find_cost(grid))

full_grid = [[((grid[j%N][i%N] + int(i/N) + int(j/N) - 1)%9 + 1) for i in range(5*N)] for j in range(5*N)]
print("Part 2:", find_cost(full_grid))
