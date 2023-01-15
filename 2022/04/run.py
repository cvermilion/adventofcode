import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

pairs = [((r[0],r[1]),(r[2],r[3])) for r in [parse("{:d}-{:d},{:d}-{:d}", l) for l in input.splitlines()]]

def covers(pair):
	# right covers left
	(p1, p2),(p3, p4) = pair
	return p1 >= p3 and p2 <= p4

def covers_either(pair):
	(pp1, pp2) = pair
	return covers((pp1, pp2)) or covers((pp2, pp1))

print("Part 1:", len(list(filter(covers_either, pairs))))

def overlaps(pair):
	(p1, p2),(p3, p4) = pair
	return (p1 >= p3 and p1 <= p4) or (p2 >= p3 and p2 <= p4) or covers_either(pair)
	
print("Part 2:", len(list(filter(overlaps, pairs))))
