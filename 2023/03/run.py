from me import *

input = get_data_2023(3)

#input = input_test

# Part A

num_pat = re.compile("\d+")
nums = [(int(m.group()), m.span()) for m in num_pat.finditer(input)]

symbol_locs = [i for (i,c) in enumerate(input) if c not in '01234567890.\n']
width = input.find("\n")+1

symbol_nabes = reduce(set.union, (set([i-1, i+1, i-width-1, i-width, i-width+1, i+width-1, i+width, i+width+1]) for i in symbol_locs))

ok_nums = [n for (n, loc) in nums if any(l in symbol_nabes for l in range(*loc))]

resultA = sum(ok_nums)

print("Part A:", resultA)
aocd.submit(resultA, part="a", day=3)

# Part B

star_locs = [i for (i,c) in enumerate(input) if c  == "*"]
# similar to above but keep separate per *
star_nabes = [set([i-1, i+1, i-width-1, i-width, i-width+1, i+width-1, i+width, i+width+1]) for i in star_locs]
star_nums = [[n for (n, loc) in nums if any(l in nabes for l in range(*loc))] for nabes in star_nabes]

resultB = sum(nn[0]*nn[1] for nn in star_nums if len(nn) == 2)
print("Part B:", resultB)
aocd.submit(resultB, part="b", day=3)
