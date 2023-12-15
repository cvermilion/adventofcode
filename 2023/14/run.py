from me import *
from sickos.yes import *
import numpy

input = get_data_2023(14)

#input = input_test

# Part A

def load(col):
	"""compute load without moving anything"""
	tot = 0
	for i,c in enumerate(col):
		if c == "O":
			idx = col[:i].rfind("#")+1
			others = col[idx:i].count("O")
			tot += len(col) - (idx+others)
	return tot
			
resultA = (
	pipeline(input.splitlines())
	| [list]
	| (lambda g: list(zip(*g)))
	| ["".join]
	| [load]
	| sum
	| DONE
)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=14)

# Part B

def rep_grid(g):
    return "\n".join("".join(row) for row in g)
    
g = numpy.array([list(l) for l in input.splitlines()])

# one initial ccw rot so N is left
g = numpy.rot90(g, 1, (0,1))

def rot(g):
	return numpy.rot90(g, 1, (1,0))
	
def find(l, el, start=0):
	for (i,x) in enumerate(l[start:]):
		if x == el:
			return i+start
	return -1

def tilt(g):
	"""shift all O's to the left through .'s but not # or O"""
	for row in g:
		dot_idx = find(row, ".")
		while dot_idx >= 0:
			o_idx = find(row, "O", dot_idx+1)
			lb_idx = find(row, "#", dot_idx+1)
			if o_idx < 0:
				break
			elif 0 <= lb_idx < o_idx:
				dot_idx = find(row, ".", lb_idx+1)
			else:
				row[dot_idx] = "O"
				row[o_idx] = "."
				dot_idx = find(row, ".", dot_idx+1)
	return g

def cycle(g):
	for _ in range(4):
		g = rot(tilt(g))
	return g

def load(g):
	return sum(sum(len(row)-i for (i,c) in enumerate(row) if c == "O") for row in g)

N = 208
for i in range(N):
	g = cycle(g)
	l = load(g)
	#print(i, l)

# test data: period is 7, 1e9%7 == 6
# real data: period is 38, after 200 load is 93114, (1e9-200)%38 == 8; after 208 load is 93102

resultB = load(g)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=14)
