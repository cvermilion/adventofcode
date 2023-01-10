from copy import deepcopy

pieces = [
	
	[[1,1,1,1]],
	
	[[0,1,0],
	 [1,1,1],
	 [0,1,0]],
	
	[[1,1,1],
	 [0,0,1],
	 [0,0,1]],
	
	[[1],
	 [1],
	 [1],
	 [1]],
	
	[[1,1],
	 [1,1]]
	
	]

input_test = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
#input = input_test
input = open("input.py").read().strip()

#chamber = [[1]*7] + [[0]*7 for _ in range(7)]
chamber = [[0]*7 for _ in range(8)]

def print_chamber(ch):
	print("\n".join("|"+"".join("@" if c else "." for c in row)+"|" for row in reversed(ch)))
	print("+-------+")

print_chamber(chamber)

def top_row(ch):
	for i, row in enumerate(ch):
		if not 1 in row:
			return i-1
	return len(ch)-1

def points(piece, offset):
	oi, oj = offset
	return sum([[(oi+i, oj+j) for (i,c) in enumerate(row) if c] for (j,row) in enumerate(piece)], [])

def print_chamber_with(ch, p, offset):
	pts = points(p, offset)
	print("\n".join("|"+"".join("@" if c or (i,j) in pts else "." for (i,c) in enumerate(row))+"|" for (j, row) in reversed(list(enumerate(ch)))))
	print("+-------+")

#print_chamber_with(chamber, pieces[0], (1,3))

def has_overlap(ch, p, offset):
	pts = points(p, offset)
	return any(ch[j][i] for (i,j) in pts)

def add_piece(ch, p, offset):
	for (i,j) in points(p, offset):
		ch[j][i] = 1

#add_piece(chamber, pieces[0], (1, 3))
#print_chamber(chamber)

#print(has_overlap(chamber, pieces[1], (2, 3)))

moves = input.strip()

def drop_piece(ch, p, move_idx):
	top = top_row(ch)
	if top + 4 + len(p) - 1 > len(ch) - 1:
		for _ in range(top + 4 + len(p) - len(ch)):
			ch.append([0]*7)
			
	offset = (2, top+4)
	
	while True:
		# do the left/right move if possible
		shift = -1 if moves[move_idx] == "<" else 1
		new_offset = (offset[0] + shift, offset[1])
		if not (new_offset[0] < 0 or new_offset[0]+len(p[0])-1 >= len(ch[0]) or has_overlap(ch, p, new_offset)):
			offset = new_offset
		move_idx += 1
		move_idx %= len(moves)
		
		# drop if possible
		new_offset = (offset[0], offset[1]-1)
		if new_offset[1] < 0 or has_overlap(ch, p, new_offset):
			# blocked, piece stops at old offset
			add_piece(ch, p, offset)
			return (move_idx, (offset[0], offset[1]-top))
		offset = new_offset

"""
drop_piece(chamber, pieces[0], 0)
print()
print_chamber(chamber)

add_piece(chamber, pieces[1], (2, top_row(chamber)+4))
print()
print_chamber(chamber)
"""

# part 1

move_idx = 0
total = 0
pieces_idx = 0
while total < 2022:
	move_idx, _ = drop_piece(chamber, pieces[pieces_idx], move_idx)
	pieces_idx += 1
	pieces_idx %= len(pieces)
	total += 1

#print_chamber(chamber)
print(top_row(chamber)+1)



# part 2

def top_row_for_col(ch, i):
	for j in range(len(ch)-1, -1, -1):
		if ch[j][i]:
			return j
	return 0

def min_top_row(ch):
	# lowest of the highest occupied row for each column
	return min(top_row_for_col(ch,i) for i in range(len(ch[0])))
	
P = len(pieces)

def height_after(n_pieces):
	chamber = [[0]*7 for _ in range(8)]
	move_idx = 0
	total = 0
	pieces_idx = 0
	height_offset = 0

	while total < n_pieces:
		move_idx, offset = drop_piece(chamber, pieces[pieces_idx], move_idx)
		pieces_idx += 1
		pieces_idx %= P
		total += 1
		
		if total % 1000 == 0:
			print(total)
			
			j = min_top_row(chamber)
			height_offset += j
			chamber = chamber[j:]
		
		if total % move_period == 0:
			print(total//move_period, "cycles")
	
	return height_offset + top_row(chamber) + 1

move_period = len(moves) * P

def find_period():
	# this is wrong!! same offsets on different substrate dont nec give the same pattern
	chamber = [[0]*7 for _ in range(8)]
	move_idx = 0
	total = 0
	pieces_idx = 0
	P = len(pieces)
	history = []
	height_offset = 0

	while True:
		move_idx, offset = drop_piece(chamber, pieces[pieces_idx], move_idx)
		pieces_idx += 1
		pieces_idx %= P
		total += 1
		history.append(offset)
		
		# check if we found a repeat
		for n in range(1,21):
			if total >= n*move_period + 10*P:
				if history[total-(n*move_period)-(10*P):total-(n*move_period)] == history[-10*P:]:
					print("found period", n, total)
					return (n, total, height_offset+top_row(chamber)+1)
		
		if total % 1000 == 0:
			print(total)
			
			j = min_top_row(chamber)
			height_offset += j
			chamber = chamber[j:]
		
		if total % move_period == 0:
			print(total//move_period, "cycles")
	
	return None

def find_period2(min, max):
	chamber = [[0]*7 for _ in range(8)]
	move_idx = 0
	total = 0
	pieces_idx = 0
	P = len(pieces)
	history = []
	height_offset = 0
	top = {}

	while total < 3*max+1000:
		move_idx, offset = drop_piece(chamber, pieces[pieces_idx], move_idx)
		pieces_idx += 1
		pieces_idx %= P
		total += 1
		#history.append(offset)
		
		if total % 1000 == 0:
			print(total)
		
		if total % move_period == 0:
			print(total//move_period, "cycles")
		
		if total >= 1000:
			j = top_row(chamber)
			top[total] = deepcopy(chamber[j-19:j+1])
			
			if total >= 1000+min:
				for period in range(min, total-1000):
					if top[total] == top[total-period]:
						return period
	"""
	for period in range(min, max+1):
		# Assume that we're cycling by 1000
		if chamber[1000:1020] == chamber[1000+period:1020+period] and chamber[1000:1020] == chamber[1000+2*period:1020+2*period]:
			return period
	"""
		
	return None
	

#print(height_after(552 + 8*move_period + 63248))
print(find_period2(1000, 5000))

"""
n, steps, top = find_period()
print("period", n, steps, top)
period = n*move_period
intro = steps - period
goal = 1000000000000
n_periods = goal // period
extra = goal % period

delta = top - height_after(intro)
full = height_after(extra) + n_periods*delta
print(full)
"""

# lazy guess: period is between 1-5k
period = find_period2(1000, 5000)
start = height_after(1000)
end = height_after(1000+period)
delta = end-start
goal = 1000000000000
n_periods = (goal-1000) // period
extra = (goal-1000) % period
rem = height_after(1000 + period + extra) - end
full = start + n_periods*delta + rem
print(full)

# too high: 1524923198852

# period 8 at 404192, h 616244
# 552 + 8 periods
# goal is 2477455*8p + 63800
# or 552 + 2477455*8p + 63248
# total: height at 63800 + 2477455*(delta for one period)
# height(552) = 830
# delta = 615414
# height(63800) 97267
# res = 1524660588637 : wrong

# height 552 + 8p + 63248 = 712673
# total = height at 552 + 2477455*delta + (height(552+8p+63248) - delta - height(552))
# res = 1524660588629 : wrong

# better test: cycle is 1725
# res = 1524637681145 : correct
