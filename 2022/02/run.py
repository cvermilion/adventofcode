input_test = """A Y
B X
C Z"""

ROCK = 1
PAPER = 2
SCISSORS = 3

left = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}
right = {'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}

scores = {
	(ROCK, ROCK): 3,
	(ROCK, PAPER): 6,
	(ROCK, SCISSORS): 0,
	(PAPER, ROCK): 0,
	(PAPER, PAPER): 3,
	(PAPER, SCISSORS): 6,
	(SCISSORS, ROCK): 6,
	(SCISSORS, PAPER): 0,
	(SCISSORS, SCISSORS): 3
	}

#input = input_test.splitlines()

input = open("input.py").readlines()

moves = [(left[l], right[r]) for (l,r) in [line.split() for line in input]]

print(sum(scores[m]+m[1] for m in moves))

better = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}
worse = dict((v,k) for (k,v) in better.items())
draw = dict((x,x) for x in better)

right = {'X': worse, 'Y': draw, 'Z': better}
moves = [(left[l], right[r][left[l]])  for (l,r) in [line.split() for line in input]]

print(sum(scores[m]+m[1] for m in moves))
