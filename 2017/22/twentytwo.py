from math import floor

text=""".##.#..#...#....###....#.
#.#######.##.##.#.##.##..
.##.#..#.###.#....###..##
......#.#..##.##...#.#.##
.#.##.##.######...##.#..#
###...#..####..######.#..
###....#....#..#####.#.##
..##..#..#.#.#.#....#####
#.#.......##.#....##..#.#
##..#.###.##.####.##...#.
#.####.##.##..##.#.##.##.
###.#..##.##.#.####...#..
######.#...#....#.#...#..
.#.#.###.##.##..#.#....##
#.###..##....###.###..#.#
.#..##.......#..#.##.##.#
..#...####...##.#.##..#.#
..#.##..#..##.###.#####.#
##..##.##....#..###.#.###
.#..######.#.####..#.###.
##...####..##.#.#.#.#.###
#.#....###...##.##..##.#.
..###.#####.####.#.#..#..
..####..#.#....#.###.....
.#......#.#..####.###...."""

text2="""..#
#..
..."""

class State (object):
	Clean =0
	Infected = 1
	Weakened = 2
	Flagged = 3

lines = text.splitlines()
grid = [[1 if c == "#" else 0 for c in l] for l in lines]

print(len(grid), len(grid[0]))
# starts 25x25 = +/- 12, center is (12,12)

def set_offset(m, i, j, x):
	offset = floor((len(m)-1)/2)
	m[j+offset][i+offset] = x

def get_offset(m, i, j):
	offset = floor((len(m)-1)/2)
	return m[j+offset][i+offset]

def contains_offset(m, i, j):
		offset = (len(m)-1)/2
		return (abs(i) <= offset) and (abs(j) <= offset)

def zero_matrix(size):
	return [[0 for i in range(size)] for j in range(size)]

def double(m):
	x_max = floor((len(m)-1)/2)
	new_size = 4*x_max + 1
	new = zero_matrix(new_size)
	for i in range(-x_max, x_max+1):
		for j in range(-x_max, x_max+1):
			set_offset(new, i, j, get_offset(m, i, j))
	return new

dirs = [(0, -1), (1,0), (0,1), (-1,0)]

def right(dir):
	idx = dirs.index(dir)
	new = (idx+1)%4
	return dirs[new]

def left(dir):
	idx = dirs.index(dir)
	new = (idx-1)%4
	return dirs[new]

def reverse(dir):
	idx = dirs.index(dir)
	new = (idx+2)%4
	return dirs[new]

def do_step(m, cur_cell, cur_dir):
	i,j = cur_cell
	state = get_offset(m, i, j)
	did_infect = False
	if state==State.Clean:
		new_dir = left(cur_dir)
		set_offset(m, i, j, State.Weakened)
	elif state==State.Weakened:
		new_dir = cur_dir
		set_offset(m, i, j, State.Infected)
		did_infect = True
	elif state==State.Infected:
		new_dir = right(cur_dir)
		set_offset(m, i, j, State.Flagged)
	else:
		new_dir = reverse(cur_dir)
		set_offset(m, i, j, State.Clean)
	di,dj = new_dir
	new_cell = (i+di,j+dj)
	if not contains_offset(m, new_cell[0], new_cell[1]):
		m = double(m)
	return m, new_cell, new_dir, did_infect

n_infects = 0
m = grid
cur = (0,0)
dir = (0,-1)
for n in range(10000000):
	m, cur, dir, did_infect = do_step(m, cur, dir)
	#print(m, cur, dir, did_infect)
	if did_infect:
		n_infects += 1

print(n_infects)
	



