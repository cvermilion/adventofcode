FILLING=3
EMPTY=4
FULL=5
FLOWING=6

class Site (object):
	def __init__(self,i,j):
		self.loc = i,j
		self.state = EMPTY
		self.visited = False
		self.bottom = False
		self.down = None
		#self.next = []
		self.left = None
		self.right = None

fmtx = "x={:d}, y={:d}..{:d}"
fmty = "y={:d}, x={:d}..{:d}"

from parse import parse
input = open("input.txt").readlines()
xdata = [parse(fmtx, l) for l in input if l.startswith("x")]
ydata = [parse(fmty, l) for l in input if l.startswith("y")]
#print(xdata)
#print(ydata)

# x vals can overflow one square
xmin = min([d[0] for d in xdata] + [d[1] for d in ydata]) - 1
xmax = max([d[0] for d in xdata] + [d[2] for d in ydata]) + 1
ymin = min([d[0] for d in ydata] + [d[1] for d in xdata])
ymax = max([d[0] for d in ydata] + [d[2] for d in xdata])
print(xmin,xmax,ymin,ymax)

#w = xmax - xmin + 1
#h = ymax - ymin + 1
real_y_min = ymin
ymin = 0

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
		y = j -ymin
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
				s.left = left
		
		if x < xmax:
			right = grid[i+1][j]
			if right:
				s.right = right

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
	imin = max(0, (500-xmin-35))-55
	imax = min(len(grid), imin+70)
	jmin=350
	jmax = min(ymax+1, 600)
	imin,jmin = 0,0
	imax = len(grid)
	jmax = len(grid[0])
	print("\n".join("".join(rep(grid[i][j]) for i in range(imin,imax)) for j in range(jmin,jmax)))
	
spring = grid[500-xmin][0-ymin]

#show()
#print()

path = [spring]
#popped_state = None
step=0
while path:
	step +=1
	#if step % 100 == 0:
		#print("step",step)
	s = path[-1]
	i,j = s.loc
	s.visited = True
	#print("dripping",i,j,s.state)
	if s.state == EMPTY:
		#print("now filling",i,j)
		s.state = FILLING
		
	if s.bottom:
		s.state = FLOWING
		path.pop()
		#popped_state = FLOWING
		continue
		#return FLOWING
	
	if s.down:
		if not s.down.visited:
			path.append(s.down)
			continue
		#if s.down.state == FILLING:
			# can we get here?
		if s.down.state == FLOWING:
			s.state = FLOWING
			path.pop()
			continue
		"""
		if s.down.state == FULL:
			if len(s.next) == 0:
				s.state = FULL
				path.pop()
				continue
		"""
	
	if s.left and not s.left.visited:
		path.append(s.left)
		continue
	if s.right and not s.right.visited:
		path.append(s.right)
		continue
		
	if (s.left and s.left.state == FLOWING) or (s.right and s.right.state == FLOWING):
		s.state = FLOWING
		# propagate flowing state the other direction if needed
		if s.right and s.right.visited and s.right.state != FLOWING and not (s.down and s.down.state == FLOWING):
			next = s.right
			while next and next.visited and not (next.down and next.down == FLOWING):
				next.state = FLOWING
				next = next.right
		if s.left and s.left.state != FLOWING:
			next = s.left
			while next and next.visited and not (next.down and next.down.state == FLOWING):
				next.state = FLOWING
				next = next.left
		path.pop()
		continue
	
	if (not s.left or s.left.state == FULL or s.left == path[-2]) and (not s.right or s.right.state == FULL or s.right == path[-2]):
		s.state = FULL
		path.pop()
		continue

	
	"""
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
	"""
		


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
"""
i=0
while spring.state != FLOWING:
	drip(spring)
	i+=1
	print(i)
"""
#show()

count = 0
full_count = 0
for i in range(len(grid)):
	for j in range(real_y_min, len(grid[0])):
		if grid[i][j] and grid[i][j].state in [FULL, FILLING, FLOWING]:
			count += 1
		if grid[i][j] and grid[i][j].state in [FULL]:
			full_count += 1
		

print(count)
print(full_count)
