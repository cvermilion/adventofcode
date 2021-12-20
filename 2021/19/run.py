data = """--- scanner 0 ---
0,2,0
4,1,0
3,3,0

--- scanner 1 ---
-1,-1,0
-5,0,0
-2,1,0"""

data = open("input_test.txt").read()
data = open("input.txt").read()

scanners = [[eval(l) for l in s.split("\n")[1:]] for s in data.strip().split("\n\n")]

def transform(i, pt):
    x,y,z = pt
    return {
        0: (x,y,z),
        1: (y,-x,z),
        2: (-x,-y,z),
        3: (-y,x,z),
        4: (x,-y,-z),
        5: (y,x,-z),
        6: (-x,y,-z),
        7: (-y,-x,-z),
        8: (-z,y,x),
        9: (y,z,x),
        10: (z,-y,x),
        11: (-y,-z,x),
        12: (z,y,-x),
        13: (-y,z,-x),
        14: (-z,-y,-x),
        15: (y,-z,-x),
        16: (x,-z,y),
        17: (z,x,y),
        18: (-x,z,y),
        19: (-z,-x,y),
        20: (x,z,-y),
        21: (-z,x,-y),
        22: (-x,-z,-y),
        23: (z,-x,-y),
    }[i]

def diff(p1, p2):
    return (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])

def add(p1, p2):
    return (p1[0]+p2[0], p1[1]+p2[1], p1[2]+p2[2])

def can_align(s1, s2):
    for t in range(24):
        pts2 = [transform(t, p) for p in s2]
        counts = {}
        for p1 in s1:
            for p2 in pts2:
                d = diff(p1, p2)
                if d in counts:
                    counts[d] += 1
                else:
                    counts[d] = 1
        for d, c in counts.items():
            if c >= 12:
                return d, t
    return None, None

locs = [None for s in scanners]
locs[0] = (0,0,0)

N = len(scanners)
while any(l is None for l in locs):
    n = len([l for l in locs if l is None])
    for i in range(N):
        if locs[i]:
            continue
        si = scanners[i]
        for j in range(N):
            if j == i:
                continue
            if not locs[j]:
                continue
            sj = scanners[j]
            # sj is known, si is unknown
            d, t = can_align(sj, si)
            if d:
                locs[i] = add(d, locs[j])
                scanners[i] = [transform(t, p) for p in si]
                break

beacons = set([])
for (l,s) in zip(locs, scanners):
    beacons = beacons.union(set(add(p, l) for p in s))

print("Part 1:", len(beacons))

# Part 2: max distance between scanners
maxd = 0
for (i, l1) in enumerate(locs):
    for (j, l2) in enumerate(locs):
        if i == j:
            continue
        d = sum(map(abs, diff(l1, l2)))
        if d > maxd:
            maxd = d

print("Part 2:", maxd)




