from me import *

input = get_data_2023(25)

#input = input_test

# Part A

class Node(object):
	def __init__(self, name, *neighbors):
		self.name = name
		self.neighbors = set(neighbors)

# jqt: rhn xhk nvd
def parse_line(l):
	node, neighbors = l.split(": ")
	return node, neighbors.split(" ")

node_data = lmap(parse_line, input.splitlines())
nodes = dict((name, Node(name)) for (name, _) in node_data)
for node, neighbors in node_data:
	for n in neighbors:
		if not n in nodes:
			nodes[n] = Node(n)
		nodes[node].neighbors.add(nodes[n])
		nodes[n].neighbors.add(nodes[node])

clusters = [(n,) for n in nodes.values()]

@cache
def n_links(c1, c2):
	tot = 0
	for n in c1:
		tot += sum(1 for nn in n.neighbors if nn in c2)
	return tot

@cache
def common_neighbors(c1, c2):
	nn1 = set.union(*(n.neighbors for n in c1))
	nn2 = set.union(*(n.neighbors for n in c2))
	return set.intersection(nn1, nn2).difference(set(c1)).difference(set(c2))

# cluster on max connections between clusters
while len(clusters) > 2:
	max_links = 0
	best = None
	if len(clusters)%100 == 0:
		print(len(clusters), "clusters")
	for (i,c1) in enumerate(clusters):
		for (j,c2) in enumerate(clusters[i+1:]):
			l = n_links(c1, c2)
			if l > max_links:
				max_links = l
				best = c1,c2
	if best is None:
		break
	c1,c2 = best
	clusters.remove(c1)
	clusters.remove(c2)
	clusters.append(c1+c2)

# merge two clusters with most common neighbors
while len(clusters) > 2:
	max_common = 0
	max_links = 0
	best = None
	if len(clusters)%100 == 0:
		print(len(clusters), "clusters")
	for (i,c1) in enumerate(clusters):
		for (j,c2) in enumerate(clusters[i+1:]):
			l = n_links(c1, c2)
			cn = len(common_neighbors(c1,c2))
			if cn > max_common:
				max_common = cn
				best = c1,c2
	if best is None:
		break
	c1,c2 = best
	clusters.remove(c1)
	clusters.remove(c2)
	clusters.append(c1+c2)


resultA = len(clusters[0])*len(clusters[1])

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=25)
