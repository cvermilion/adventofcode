input = open("input.txt").readlines()
from parse import parse
pts = [parse("{:d},{:d},{:d},{:d}", l).fixed for l in input]

def dist(p1, p2):
	return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2]) + abs(p1[3]-p2[3])

neighbors = dict((p, set(p2 for p2 in pts if dist(p,p2) <= 3)) for p in pts)

clusters = []
while neighbors:
	first = list(neighbors.keys())[0]
	clu = set([first])
	to_add = neighbors[first]
	del neighbors[first]
	while to_add:
		for pt in list(to_add):
			if pt not in clu:
				clu.add(pt)
				to_add.update(neighbors[pt])
				del neighbors[pt]
		to_add.difference_update(clu)
	clusters.append(clu)
	
print(len(clusters))
	
