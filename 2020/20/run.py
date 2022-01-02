from parse import parse
import functools
import operator
import math

def parse_tile(s):
	lines = s.splitlines()
	n = parse("Tile {:d}:", lines[0])[0]
	grid = [[1 if c == "#" else 0 for c in l] for l in lines[1:]]
	return n, grid

data = open("input.py").read()
tiles = [parse_tile(s) for s in data.split("\n\n")]
tiles = dict((t[0], t[1]) for t in tiles)

def rep(g):
	return "\n".join("".join(map(str, row)) for row in g)

def borders(grid):
	digs = [
		grid[0],
		[grid[j][len(grid[j])-1] for j in range(len(grid))],
		grid[len(grid)-1],
		[grid[j][0] for j in range(len(grid))],
		]
	digs = digs + [reversed(dd) for dd in digs]
	return [int("".join(str(c) for c in dd), 2) for dd in digs]

def rotate(grid, n):
	# n clockwise rotations
	N = len(grid)
	for nn in range(n):
		grid = [[grid[N-i-1][j] for i in range(N)] for j in range(N)]
	return grid

def flip(grid):
	N = len(grid)
	return [grid[N-j-1] for j in range(N)]

all_borders = sum([borders(t) for t in tiles.values()], [])
bb = dict((n, borders(t)) for (n,t) in tiles.items())
uniqs = [b for (i,b) in enumerate(all_borders) if b not in all_borders[:i] and b not in all_borders[i+1:]]

# For Part 1: only need to find the tiles with two unique border codes
corners = [i for (i,b) in bb.items() if len([n for n in b if n in uniqs]) == 4] # borders includes reverses

print("Part 1:", functools.reduce(operator.mul, corners, 1))

# Part 2: now we have to actually find the full grid
N = int(math.sqrt(len(tiles)))
full = [[None for i in range(N)] for j in range(N)]
# start with one corner, which fixes the overall orientation (which is arbitrary)
# may need to rotate to put the uniques on the corner
b = bb[corners[0]]
cc = tuple([i for (i,id) in enumerate(b[:4]) if id in uniqs])
rot = {(0,1): 3, (1,2): 2, (2,3): 1, (0,3): 0}[cc]
full[0][0] = corners[0], rotate(tiles[corners[0]], rot)

for j in range(N):
	for i in range(N):
		if full[j][i]:
			continue
		if i > 0:
			left_id, left_tile = full[j][i-1]
			left_border = int("".join(map(str, (left_tile[jj][len(left_tile)-1] for jj in range(len(left_tile))))),2)
			
			right_id, right = [(n,b) for (n, b) in bb.items() if n != left_id and left_border in b][0]
			rtile = tiles[right_id]
			if left_border == right[3]:
				full[j][i] = right_id, rtile
			elif left_border == right[2]:
				full[j][i] = right_id, rotate(rtile, 1)
			elif left_border == right[1+4]:
				full[j][i] = right_id, rotate(rtile, 2)
			elif left_border == right[0+4]:
				full[j][i] = right_id, rotate(rtile, 3)
			elif left_border == right[3+4]:
				full[j][i] = right_id, flip(rtile)
			elif left_border == right[2+4]:
				full[j][i] = right_id, flip(rotate(rtile, 1))
			elif left_border == right[1]:
				full[j][i] = right_id, flip(rotate(rtile, 2))
			elif left_border == right[0]:
				full[j][i] = right_id, flip(rotate(rtile, 3))
		else:
			top_id, top_tile = full[j-1][i]
			top = bb[top_id]
			top_border = int("".join(map(str, (top_tile[len(top_tile)-1][ii] for ii in range(len(top_tile))))),2)
			
			bottom_id, bottom = [(n,b) for (n, b) in bb.items() if n != top_id and top_border in b][0]
			btile = tiles[bottom_id]
			if top_border == bottom[0]:
				full[j][i] = bottom_id, btile
			elif top_border == bottom[3+4]:
				full[j][i] = bottom_id, rotate(btile, 1)
			elif top_border == bottom[2+4]:
				full[j][i] = bottom_id, rotate(btile, 2)
			elif top_border == bottom[1]:
				full[j][i] = bottom_id, rotate(btile, 3)
			elif top_border == bottom[0+4]:
				full[j][i] = bottom_id, flip(rotate(btile, 2))
			elif top_border == bottom[3]:
				full[j][i] = bottom_id, flip(rotate(btile, 3))
			elif top_border == bottom[2]:
				full[j][i] = bottom_id, flip(btile)
			elif top_border == bottom[1+4]:
				full[j][i] = bottom_id, flip(rotate(btile, 1))

# finally, assemble the image
img = [[None for i in range(N)] for j in range(N)]
# fill in properly oriented tiles
for i in range(N):
	for j in range(N):
		# trim off border
		tile = full[j][i][1]
		img[j][i] = [row[1:-1] for row in tile[1:-1]]

# now combine into one big grid
img = sum([[sum([tile[j] for tile in row], []) for j in range(len(row[0]))] for row in img], [])

monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".strip("\n")
monster = [[1 if c == "#" else 0 for c in l] for l in monster.splitlines()]

def find_matches(grid, pattern):
	matches = []
	for j in range(len(grid)-len(pattern)+1):
		for i in range(len(grid[0])-len(pattern[0])+1):
			if all(all(not pattern[jj][ii] or grid[j+jj][i+ii] for ii in range(len(pattern[0]))) for jj in range(len(pattern))):
				matches.append((i,j))
	return matches

total = 0
# Add the number of monsters found for each rotation and flip of the original image. Note that the lack of symmetry in the sea monster pattern means that exactly one orientation can match any given monster in the image
for rot in range(4):
	m = find_matches(rotate(img, rot), monster)
	total += len(m)
	m = find_matches(flip(rotate(img, rot)), monster)
	total += len(m)

# Here we assume that the sea monsters never overlap so we can take their total footprint to just be N times the footprint of one.
all_count = sum(sum(img, []))
len_monster = sum(sum(monster, []))
result = all_count - total*len_monster
print("Part 2:", result)

