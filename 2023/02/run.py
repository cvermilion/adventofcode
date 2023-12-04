from me import *

input = get_data_2023(2)

#input = input_test

# Part 1

def parse_game(s):
	return dict(pipe(
	  s.strip().split(","),
	  str.strip,
	  [str.split, " "],
	  lambda ss: [ss[1], int(ss[0])]
	))

def parse_line(s):
	n = int(s.split(":")[0].split(" ")[1])
	return n, list(pipe(
		s.split(":")[1].strip().split(";"),
		parse_game
	))
	
max_balls = {"red": 12, "blue": 14, "green": 13}

def allowed_show(s):
	return all(v <= max_balls[k] for (k,v) in s.items())

games = lmap(parse_line, input.splitlines())
allowed = filter(lambda g: all(map(allowed_show, g[1])), games)

resultA = sum(a[0] for a in allowed)



""" 
result1 = sum(pipe(
	input.splitlines(),
	partial(filter, is_dig),
	partial(lmap, int),
	lambda dd: 10*dd[0]+dd[-1]
))
"""

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=2)

# part 2

def min_set(game):
	return dict((col, max(show.get(col, 0)for show in game[1])) for col in ["red", "green", "blue"])

def power(d):
	return reduce(mul, d.values())

resultB = sum(power(min_set(g)) for g in games)
print("Part B:", resultB)
#aocd.submit(resultB, part="B", day=2)
