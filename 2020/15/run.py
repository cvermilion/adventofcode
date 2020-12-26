from functools import reduce

#nums = [6,3,0]
nums = [4,1,20,6,14,0]

def step(l):
    last = l[0]
    if not last in l[1:]:
        return [0] + l
    idx = l[1:].index(last)+1
    return [idx] + l

print("Part 1:", reduce(lambda acc,x:step(acc), range(2020-len(nums)), nums)[0])

# Need a fast approach for Part 2.

# Solution: store the last number, and a dict of seen numbers with their most recent index

#nums = [0,3]
#last = 6
nums = [0,14,6,20,1]
last = 4
last_idx = dict((n,i) for (i,n) in enumerate(nums))
n = len(nums) # "most recent" index is n - index in last_idx
while n < 30000000-1:
    last_seen = last_idx.get(last)
    last_idx[last] = n
    if last_seen is None:
        last = 0
    else:
        last = n - last_seen
    n += 1

print("Part 2:", last)
