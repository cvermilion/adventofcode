#!/usr/bin/env python3

with open("input.txt") as f:
    text = f.read()

offsets = list(map(int, text.split()))

def advance(cur, offsets):
    nxt = cur + offsets[cur]
    if nxt < 0 or nxt >= len(offsets):
        return -1
    offsets[cur] += 1
    return nxt

def advance2(cur, offsets):
    nxt = cur + offsets[cur]
    if nxt < 0 or nxt >= len(offsets):
        return -1

    delta = -1 if offsets[cur] >= 3 else 1
    offsets[cur] = offsets[cur] + delta
    return nxt

def nsteps(advancer):
    local_offsets = offsets[:]
    ctr=0
    nxt=0
    while nxt != -1:
        nxt = advancer(nxt, local_offsets)
        ctr+=1
    return ctr

print("Part 1: {:d}", nsteps(advance))
print("Part 2: {:d}", nsteps(advance2))
