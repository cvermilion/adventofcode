from functools import reduce
from operator import mul

nums = [int(l) for l in open("input.txt")]

nums.sort()
nums = [0] + nums + [nums[-1]+3]
diffs = [nums[i+1]-nums[i] for i in range(len(nums)-1)]

ones = len([n for n in diffs if n == 1])
threes = len([n for n in diffs if n == 3])

print("Part 1:", ones * threes)

# Part 2: how many ways can we chain the adapters?

""" The key thing for this part is to represent the all-adapter chain
as a list of gaps, and see the following:

    [1, 1, 1, 3, 1, 1, 3, ... ]

    * The input only contains gaps of 1 or 3
    * Every gap of 3 is unbridgable -- you can't remove either end because
      you'd have a gap of more than 3.
    * Two gaps of 1 means you can drop the middle adapter and have a gap
      of 2. [... 1, 1 ... ] => [ ... 2 ... ]
    * A gap of 1 and a gap of 2 can likewise be merged to a 3:
        [ ... 1, 2 ... ] => [ ... 3 ... ]
    * The problem _factorizes_ due to the 3's not being droppable -- just
      compute the number of ways you can combine each block of ones and then
      just multiply all the blocks.
"""

def combinations(nums):
    """The set of ways you can combine a list of diffs.

    Could optimize further by a) memoizing, and b) factorizing sublists if we hit a 3.
    """
    # split on 3's
    if 3 in nums:
       sublists = [tuple([int(c) for c in group]) for group in ''.join(str(i) for i in nums).split('3')]
       return reduce(mul, (combinations(nn) for nn in sublists))

    # now, generate all shorter lists
    seen = set([nums])
    next_to_check = set([nums])
    while next_to_check:
        to_check = next_to_check
        next_to_check = set()
        for nn in to_check:
            for i in range(len(nn)-1):
                if nn[i] + nn[i+1] <= 3:
                    merged = tuple(list(nn[:i]) + [nn[i]+nn[i+1]] + list(nn[i+2:]))
                    if not merged in seen:
                        next_to_check.add(merged)
                        seen.add(merged)

    res = len(seen)
    return res

print("Part 2:", combinations(diffs))
