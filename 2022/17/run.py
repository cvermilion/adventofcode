import os, sys
sys.path.append(os.path.realpath(".."))
from util import *
from queue import PriorityQueue
from collections import namedtuple
from copy import deepcopy

#test()
input = get_input()

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

moves = input.strip()

chamber = [[0]*7 for _ in range(8)]

def print_chamber(ch):
	print("\n".join("|"+"".join("@" if c else "." for c in row)+"|" for row in reversed(ch)))
	print("+-------+")

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

def has_overlap(ch, p, offset):
	pts = points(p, offset)
	return any(ch[j][i] for (i,j) in pts)

def add_piece(ch, p, offset):
	for (i,j) in points(p, offset):
		ch[j][i] = 1

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

# part 1

move_idx = 0
total = 0
pieces_idx = 0
while total < 2022:
	move_idx, _ = drop_piece(chamber, pieces[pieces_idx], move_idx)
	pieces_idx += 1
	pieces_idx %= len(pieces)
	total += 1

print("Part 1:", top_row(chamber)+1)

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
			#print(total)
			
			j = min_top_row(chamber)
			height_offset += j
			chamber = chamber[j:]
		
		#if total % move_period == 0:
		#	print(total//move_period, "cycles")
	
	return height_offset + top_row(chamber) + 1

move_period = len(moves) * P

def find_period_bad():
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

def find_period(min, max):
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
		
		#if total % 1000 == 0:
		#	print(total)
		
		#if total % move_period == 0:
		#	print(total//move_period, "cycles")
		
		if total >= 1000:
			j = top_row(chamber)
			top[total] = deepcopy(chamber[j-19:j+1])
			
			if total >= 1000+min:
				for period in range(min, total-1000):
					if top[total] == top[total-period]:
						return period
		
	return None

# lazy guess: period is between 1-5k
period = find_period(1000, 5000)
start = height_after(1000)
end = height_after(1000+period)
delta = end-start
goal = 1000000000000
n_periods = (goal-1000) // period
extra = (goal-1000) % period
rem = height_after(1000 + period + extra) - end
full = start + n_periods*delta + rem
print("Part 2:", full)
