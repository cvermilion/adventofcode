from functools import reduce
from operator import mul

l1,l2 = open("input.txt").readlines()
start = int(l1)
buses = [int(s) for s in l2.split(",") if s != "x"]

def wait(bus):
    prev = int(start / bus)
    if prev*bus == start:
        return 0
    return (prev+1)*bus - start

minb, min_wait = min(((b, wait(b)) for b in buses), key=lambda x:x[1])
print("Part 1:", minb*min_wait)

# Part 2
# Approach: the solution for N buses is also a solution for N-1, so to find
# a solution for N, we iterate through solutions of N-1 and check.

# Also grab the offset for each bus, and then sort descending by period for faster search
buses = [(i, int(s)) for (i,s) in enumerate(l2.split(",")) if s != "x"]
buses.sort(key=lambda x:x[1])
buses = list(reversed(buses))

# First: the solution for just one bus is t = (period - offset)
sol1 = buses[0][1] - buses[0][0]
nsolved = 1
next_sol = sol1

# Now, iteratively find a solution for N+1 buses
while nsolved < len(buses):
    total_period = reduce(mul, [b[1] for b in buses[:nsolved]])
    offset, period = buses[nsolved]
    while True:
        # is sol for bus n+1?
        if (next_sol + offset)%period == 0:
            break
        next_sol += total_period
    nsolved += 1

print("Part 2:", next_sol)
