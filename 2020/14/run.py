from functools import reduce
from operator import mul
from parse import parse

lines = open("input.txt").readlines()

def parse_op(s):
    res = parse("mem[{:d}] = {:d}", s)
    return res[0], res[1]

def parse_mask(s):
    b = s[7:].strip() 
    mask = b.replace("1", "0").replace("X", "1")
    value = b.replace("X", "0")
    return int(mask, 2), int(value, 2)

def apply_mask(m, v, x):
    return (m&x) + v

mask, value = 0, 0
vals = {}
for l in lines:
    if l.startswith("mask"):
        mask, value = parse_mask(l)
    else:
        addr, x = parse_op(l)
        vals[addr] = apply_mask(mask, value, x)

print("Part 1:", sum(vals.values()))

def parse_mask2(s):
    b = s[7:].strip()
    # applying mask is zeroing out the X bits, then OR with the remaining
    # ie, masked = (addr & mask1) | mask2
    mask1 = int(b.replace("0", "1").replace("X", "0"), 2)
    mask2 = int(b.replace("X", "0"), 2)
    # indices of x's
    xs = [i for (i,c) in enumerate(reversed(b)) if c == "X"]
    return mask1, mask2, xs

# for a set of floating bits, return the list of values to add to the masked addr
# to get the full set of all addresses
def addrs_to_add(xs):
    addrs = []
    for n in range(2**len(xs)):
        digits = [int(c) for c in reversed("{:b}".format(n))]
        addr = sum(2**(xs[i]) if d else 0 for (i,d) in enumerate(digits))
        addrs.append(addr)
    return addrs

vals = {}
m1, m2, addrs = 0, 0, []

for l in lines:
    if l.startswith("mask"):
        m1, m2, xs = parse_mask2(l)
        addrs = addrs_to_add(xs)
    else:
        addr, x = parse_op(l)
        masked = (addr & m1) | m2
        for a in addrs:
            vals[masked + a] = x

print("Part 2:", sum(vals.values()))



