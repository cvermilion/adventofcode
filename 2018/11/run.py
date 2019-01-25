def hundreds(x):
	x = x % 1000
	return int(x / 100)
	
def power(x,y):
	rackID = x+10
	val = ((rackID*y)+7989)*rackID
	return hundreds(val)-5
	

grid = [[power(x,y) for y in range(1,301)] for x in range(1, 301)]

def square(x,y,n):
	return sum(sum([r[y:y+n] for r in grid[x:x+n]], []))

print(square(0,0,3))

#squares = [[square(i,j,2) for j in range(299)] for i in range(299)]
from copy import deepcopy
squares = deepcopy(grid)

# what to add to square i,j to go from n to n+1
def extend(i,j,n):
	return sum(grid[i+ii][j+n] for ii in range(n)) + sum(grid[i+n][j+jj] for jj in range(n)) + grid[i+n][j+n]

best = square(0,0,2)
m = (1,1)
for n in range(1,300):
	print(n+1)
	for i in range(300-n):
		for j in range(300-n):
			s = squares[i][j] + extend(i,j,n)
			squares[i][j] = s
			#s = square(i,j,n)
			if s > best:
				best = s
				m = (i+1,j+1), n+1

print(m,best)
#print(square(18,16,3))
