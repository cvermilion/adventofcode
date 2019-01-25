FILLING=3
EMPTY=4
FULL=5
FLOWING=6

class Site (object):
	def __init__(self,i,j):
		self.loc = i,j
		self.state = EMPTY
		self.bottom = False
		self.down = None
		self.next = []

fmtx = "x={:d}, y={:d}..{:d}"
fmty = "y={:d}, x={:d}..{:d}"

from parse import parse
input = open("test.txt").readlines()
xdata = [parse(fmtx, l) for l in input if l.startswith("x")]
ydata = [parse(fmty, l) for l in input if l.startswith("y")]
#print(xdata)
#print(ydata)

# x vals can overflow one square
xmin = min([d[0] for d in xdata] + [d[1] for d in ydata]) - 1
xmax = max([d[0] for d in xdata] + [d[2] for d in ydata]) + 1
ymin = min([d[0] for d in ydata] + [d[1] for d in xdata] + [0])
ymax = max([d[0] for d in ydata] + [d[2] for d in xdata])
print(xmin,xmax,ymin,ymax)

w = xmax - xmin + 1
h = ymax - ymin + 1

grid = [[Site(i-xmin,j-ymin) for j in range(ymin,ymax+1)] for i in range(xmin, xmax+1)]

for xd in xdata:
	x = xd[0]
	i = x - xmin
	for y in range(xd[1], xd[2]+1):
		j = y - ymin
		grid[i][j] = None # marks wall
		
for yd in ydata:
	y = yd[0]
	j = y - ymin
	for x in range(yd[1], yd[2]+1):
		i = x - xmin
		grid[i][j] = None # marks wall
		
# Use Site.next to mark where water can flow
for i in range(len(grid)):
	x = xmin + i
	for j in range(len(grid[0])):
		y = ymin + j
		s = grid[i][j]
		if not s:
			continue
		if y == ymax:
			s.bottom = True
			continue
		
		down = grid[i][j+1]
		if down:
			s.down = down
		
		if i > 0:
			left = grid[i-1][j]
			if left:
				s.next.append(left)
		
		if x < xmax:
			right = grid[i+1][j]
			if right:
				s.next.append(right)

spring = grid[500-xmin][0-ymin]

def drip(s):
	i,j = s.loc
	#print("dripping",i,j,s.state)
	if s.state == EMPTY:
		#print("now filling",i,j)
		s.state = FILLING
		
	if s.bottom:
		s.state = FLOWING
		return FLOWING
	
	if s.down:
		state = drip(s.down)
		if state == FLOWING:
			s.state = FLOWING
			s.down = None
			return FLOWING
		elif state == FULL:
			s.down = None
		else:
			return FILLING
	
	if len(s.next) == 0:
		if s.state != FULL:
			s.state = FULL
		return FULL
	
	next = s.next[0]
	# exclude s from next's next
	next.next = [n for n in next.next if n != s]
	
	state = drip(next)
	if state == FILLING:
		return FILLING
	elif state == FLOWING:
		s.next = s.next[1:]
		if len(s.next) == 0:
			s.state = FLOWING
			return FLOWING
		return FILLING
	elif state == FULL:
		s.next = s.next[1:]
		if len(s.next) == 0:
			s.state = FULL
			return FULL
		return FILLING
		
def rep(cell):
	if not cell:
		return "#"
	if cell.state == FULL:
		return "~"
	if cell.state in [FILLING]:
		return "|"
	if cell.state == FLOWING:
		return "v"
	return "."
	
def show():
	print("\n".join("".join(rep(grid[i][j]) for i in range(len(grid))) for j in range(len(grid[0]))))

"""
show()
print()
drip(spring)
show()
print()
i=0
while i < 5:
	drip(spring)
	print()
	show()
	i+=1
#show()
"""
i=0
while spring.state != FLOWING:
	drip(spring)
	i+=1
	print(i)

count = 0
for i in range(len(grid)):
	for j in range(len(grid[0])):
		if grid[i][j] and grid[i][j].state in [FULL, FILLING, FLOWING]:
			count += 1

# spring itself doesnt count
print(count-1)
