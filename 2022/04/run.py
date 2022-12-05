input_text = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

#input = input_text.splitlines()
input = open("input.py").readlines()

from parse import parse

pairs = [((r[0],r[1]),(r[2],r[3])) for r in [parse("{:d}-{:d},{:d}-{:d}", l) for l in input]]

def covers(pair):
	# right covers left
	(p1, p2),(p3, p4) = pair
	return p1 >= p3 and p2 <= p4

def covers_either(pair):
	(pp1, pp2) = pair
	return covers((pp1, pp2)) or covers((pp2, pp1))

print(len(list(filter(covers_either, pairs))))

def overlaps(pair):
	(p1, p2),(p3, p4) = pair
	return (p1 >= p3 and p1 <= p4) or (p2 >= p3 and p2 <= p4) or covers_either(pair)
	
print(len(list(filter(overlaps, pairs))))
