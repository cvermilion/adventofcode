from me import *

input = get_data_2023(2)

#input = input_test

# Part A

def parse_show(s):
	return dict(pipe(
	  s.strip().split(","),
	  str.strip,
	  [str.split, " "],
	  lambda ss: [ss[1], int(ss[0])]
	))

def parse_line(l):
	return lmap(parse_show, l.split(":")[1].strip().split(";"))
	
max_balls = {"red": 12, "blue": 14, "green": 13}

def allowed_show(s):
	return all(v <= max_balls[k] for (k,v) in s.items())

games = lmap(parse_line, input.splitlines())

resultA = sum(i+1 for (i,g) in enumerate(games) if all(map(allowed_show, g)))

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=2)

# Part B

def min_set(game):
	return dict((col, max(show.get(col, 0)for show in game)) for col in ["red", "green", "blue"])

def power(d):
	return reduce(mul, d.values())

resultB = sum(power(min_set(g)) for g in games)
print("Part B:", resultB)
#aocd.submit(resultB, part="B", day=2)
