from parse import parse
from math import copysign

steps = [parse("{}{:d}", l) for l in open("input.txt")]

# state = [direction, position]
init_state = [(1,0), (0,0)]

dirs = [(1,0), (0,-1), (-1, 0), (0, 1)]
dirIndices = dict((d, i) for (i,d) in enumerate(dirs))

def rotate(d, degrees):
    n = int(degrees / 90)
    return dirs[(dirIndices[d] + n)%4]

ops = {
    "F": (lambda st,x: (st[0], (st[1][0] + st[0][0]*x, st[1][1] + st[0][1]*x))),
    "E": (lambda st,x: (st[0], (st[1][0]+x, st[1][1]))),
    "W": (lambda st,x: (st[0], (st[1][0]-x, st[1][1]))),
    "N": (lambda st,x: (st[0], (st[1][0], st[1][1]+x))),
    "S": (lambda st,x: (st[0], (st[1][0], st[1][1]-x))),
    "R": (lambda st,x: (rotate(st[0], x), st[1])),
    "L": (lambda st,x: (rotate(st[0], -x), st[1])),
}

st = init_state
for s in steps:
    st = ops[s[0]](st, s[1])

print("Part 1:", abs(st[1][0]) + abs(st[1][1]))

# Part 2: now we track a waypoint *and* the ship

# state = [position, waypoint]
init_state = [(0,0), (10,1)]

def sign(x):
    if x == 0:
        return 0
    return copysign(1, x)

def rotate_wp(wp, degrees):
    d1 = (sign(wp[0]), 0)
    d2 = (0, sign(wp[1]))
    n = int(degrees / 90)
    newd1 = dirs[(dirIndices[d1] + n)%4] if d1 != (0,0) else (0,0)
    newd2 = dirs[(dirIndices[d2] + n)%4] if d2 != (0,0) else (0,0)
    return (abs(wp[0])*newd1[0] + abs(wp[1])*newd2[0], abs(wp[0])*newd1[1] + abs(wp[1])*newd2[1])

ops = {
    "E": (lambda st,x: (st[0], (st[1][0]+x, st[1][1]))),
    "W": (lambda st,x: (st[0], (st[1][0]-x, st[1][1]))),
    "N": (lambda st,x: (st[0], (st[1][0], st[1][1]+x))),
    "S": (lambda st,x: (st[0], (st[1][0], st[1][1]-x))),
    "F": (lambda st,x: ((st[0][0] + st[1][0]*x, st[0][1] + st[1][1]*x), st[1])),
    "R": (lambda st,x: (st[0], rotate_wp(st[1], x))),
    "L": (lambda st,x: (st[0], rotate_wp(st[1], -x))),
}

st = init_state
for s in steps:
    st = ops[s[0]](st, s[1])

print("Part 2:", abs(st[0][0]) + abs(st[0][1]))
