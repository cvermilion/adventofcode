from parse import parse
from functools import reduce
from operator import mul

grid = open("input.txt").readlines()
w = len(grid[0])-1 # -1 to ignore the terminal newline

print("Part 1: ", sum(1 if l[(3*j)%w] == "#" else 0 for (j,l) in enumerate(grid)))

slopes = [[1,1], [1,3], [1,5], [1,7], [2,1]]

def count_for_slope(s):
    return sum(1 if l[(s[1]*j)%w] == "#" else 0 for (j,l) in enumerate(grid[::s[0]]))

print("Part 2: ", reduce(mul, [count_for_slope(s) for s in slopes], 1))

