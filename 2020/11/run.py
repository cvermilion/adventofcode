from copy import deepcopy

FLOOR=0
FULL=1
EMPTY=2

typ = {".": FLOOR, "#": FULL, "L": EMPTY}
rep = {FLOOR: ".", FULL: "#", EMPTY: "L"}
grid = [[typ[c] for c in l.strip()] for l in open("input.txt")]

def rep_grid(g):
    return "\n".join("".join(rep[el] for el in row) for row in g)

def nabes(i,j):
    nn = []
    if i > 0:
        nn.append([i-1, j])
        if j > 0:
            nn.append([i-1, j-1])
        if j < len(grid)-1:
            nn.append([i-1, j+1])
    if i < len(grid[0])-1:
        nn.append([i+1, j])
        if j > 0:
            nn.append([i+1, j-1])
        if j < len(grid)-1:
            nn.append([i+1, j+1])
    if j > 0:
        nn.append([i, j-1])
    if j < len(grid)-1:
        nn.append([i, j+1])
    return nn

def sum_nabes(g, i, j):
    return sum(el for el in [g[jj][ii] for (ii,jj) in nabes(i,j)] if el == FULL)

def step(g):
    next_g = deepcopy(g)
    for j in range(len(g)):
        for i in range(len(g[0])):
            if g[j][i] == EMPTY and sum_nabes(g, i, j) == 0:
                next_g[j][i] = FULL
            elif g[j][i] == FULL and sum_nabes(g, i, j) >= 4:
                next_g[j][i] = EMPTY
    return next_g

cur_g = grid
next_g = step(grid)
while next_g != cur_g:
    cur_g = next_g
    next_g = step(next_g)

print("Part 1:", sum(sum(el for el in row if el == FULL) for row in cur_g))
            

def visible_nabes(g, i, j):
    dirs = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)]
    nn = []
    # traverse in each direction until we find a seat or the end of the grid
    for (di,dj) in dirs:
        ii,jj = i+di,j+dj
        while ii >=0 and ii < len(g[0]) and jj >= 0 and jj < len(g) and g[jj][ii] == FLOOR:
            ii,jj = ii+di,jj+dj
        if ii >=0 and ii < len(g[0]) and jj >= 0 and jj < len(g):
            nn.append((ii,jj))
    return nn

def sum_nabes2(g, i, j):
    return sum(el for el in [g[jj][ii] for (ii,jj) in visible_nabes(g,i,j)] if el == FULL)

def step2(g):
    next_g = deepcopy(g)
    for j in range(len(g)):
        for i in range(len(g[0])):
            if g[j][i] == EMPTY and sum_nabes2(g, i, j) == 0:
                next_g[j][i] = FULL
            elif g[j][i] == FULL and sum_nabes2(g, i, j) >= 5:
                next_g[j][i] = EMPTY
    return next_g

cur_g = grid
next_g = step2(grid)
while next_g != cur_g:
    cur_g = next_g
    next_g = step2(next_g)


print("Part 2:", sum(sum(el for el in row if el == FULL) for row in cur_g))
