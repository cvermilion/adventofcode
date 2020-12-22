from copy import deepcopy

grid = [[[1 if c == '#' else 0 for c in l.strip()] for l in open("input.txt")]]

def pad(g):
    nZ = len(g) + 2
    nY = len(g[0]) + 2
    nX = len(g[0][0]) + 2
    newG = [[[0 for i in range(nX)] for j in range(nY)] for k in range(nZ)]
    for i in range(nX-2):
        for j in range(nY-2):
            for k in range(nZ-2):
                if g[k][j][i]:
                    newG[k+1][j+1][i+1] = 1
    return newG

def flatten2(l):
    l = [item for subl in l for item in subl]
    return [item for subl in l for item in subl]


def sum_neighbors(g, i, j, k):
    nabes = [[g[kk][jj][i-1:i+2] for jj in range(j-1, j+2)] for kk in range(k-1, k+2)]
    return sum(flatten2(nabes)) - g[k][j][i]

def step(g):
    orig = pad(g)
    newG = deepcopy(orig)
    for i in range(1, len(newG[0][0])-1):
        for j in range(1, len(newG[0])-1):
            for k in range(1, len(newG)-1):
                sumN = sum_neighbors(orig, i, j, k)
                if orig[k][j][i] and sumN not in [2,3]:
                    newG[k][j][i] = 0
                elif not orig[k][j][i] and sumN == 3:
                    newG[k][j][i] = 1
    return newG


def repG(g):
    return "\n\n".join("\n".join("".join("#" if el else "." for el in l) for l in plane) for plane in g)

def repNabes(g):
    return "\n\n".join("\n".join("".join(str(el) for el in l) for l in plane) for plane in g)

def fillNabes(g):
    orig = pad(g)
    newG = deepcopy(orig)
    for i in range(1, len(newG[0][0])-1):
        for j in range(1, len(newG[0])-1):
            for k in range(1, len(newG)-1):
                sumN = sum_neighbors(orig, i, j, k)
                newG[k][j][i] = sumN
    return newG

print(repG(grid))
print()
    
print("Part 1:", sum(flatten2(step(step(step(step(step(step(pad(grid))))))))))


grid2 = [[[[1 if c == '#' else 0 for c in l.strip()] for l in open("input.txt")]]]

def pad2(g):
    nA = len(g) + 2
    nZ = len(g[0]) + 2
    nY = len(g[0][0]) + 2
    nX = len(g[0][0][0]) + 2
    newG = [[[[0 for i in range(nX)] for j in range(nY)] for k in range(nZ)] for l in range(nA)]
    for i in range(nX-2):
        for j in range(nY-2):
            for k in range(nZ-2):
                for l in range(nA-2):
                    if g[l][k][j][i]:
                        newG[l+1][k+1][j+1][i+1] = 1
    return newG

def flatten3(l):
    l = [item for subl in l for item in subl]
    l = [item for subl in l for item in subl]
    return [item for subl in l for item in subl]


def sum_neighbors2(g, i, j, k, l):
    nabes = [[[g[ll][kk][jj][i-1:i+2] for jj in range(j-1, j+2)] for kk in range(k-1, k+2)] for ll in range(l-1, l+2)]
    return sum(flatten3(nabes)) - g[l][k][j][i]

def step2(g):
    orig = pad2(g)
    newG = deepcopy(orig)
    for i in range(1, len(newG[0][0][0])-1):
        for j in range(1, len(newG[0][0])-1):
            for k in range(1, len(newG[0])-1):
                for l in range(1, len(newG)-1):
                    sumN = sum_neighbors2(orig, i, j, k, l)
                    if orig[l][k][j][i] and sumN not in [2,3]:
                        newG[l][k][j][i] = 0
                    elif not orig[l][k][j][i] and sumN == 3:
                        newG[l][k][j][i] = 1
    return newG


print("Part 2:", sum(flatten3(step2(step2(step2(step2(step2(step2(pad2(grid2))))))))))
