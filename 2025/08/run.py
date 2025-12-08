from me import *
from sickos.yes import *
from queue import PriorityQueue
from operator import mul

DAY=8

input = get_data_2025(DAY)
steps = 1000

input = input_test
steps = 10

VecT = namedtuple("Vec", "x y z")

class Vec(VecT):
	def mag2(self):
		return self.x**2 + self.y**2 + self.z**2
	
	def __sub__(self, v2):
		return Vec(self.x-v2.x, self.y-v2.y, self.z-v2.z)

# Part 1

pts = (pipeline(input.splitlines())
	| [(str.split, ",")]
	| [[int]]
	| [splat(Vec)]
	| DONE)
	
circuits = dict((v, {v}) for v in pts)
to_check = PriorityQueue()

for (i,v1) in enumerate(pts):
	for v2 in pts[i+1:]:
		to_check.put(((v2-v1).mag2(), (v1,v2)))

for _ in range(steps):
	(_, (v1,v2)) = to_check.get()
	if v2 not in circuits[v1]:
		circuits[v1].update(circuits[v2])
		for c in circuits[v2]:
			circuits[c] = circuits[v1]

# now find biggest N

unique = dict((id(c), c) for c in circuits.values()).values()

sizes = sorted(lmap(len, unique))

result1 = reduce(mul, sizes[-3:], 1)
print("Part 1:", result1)
#aocd.submit(result1, part="a", day=DAY)

# Part 2

# now just keep going til we're done
while not to_check.empty():
	(_, (v1,v2)) = to_check.get()
	if v2 not in circuits[v1]:
		circuits[v1].update(circuits[v2])
		if len(circuits[v1]) == len(pts):
			result2 = v1.x * v2.x
			break
		for c in circuits[v2]:
			circuits[c] = circuits[v1]

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=DAY)