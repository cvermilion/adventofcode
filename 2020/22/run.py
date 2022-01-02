from collections import deque

data = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

data = open("input.py").read()

p1, p2 = data.split("\n\n")
p1, p2 = [deque(int(s) for s in p.splitlines()[1:]) for p in [p1,p2]]

def turn(p1, p2):
	c1, c2 = p1.popleft(), p2.popleft()
	if c1 > c2:
		p1.extend([c1, c2])
	else:
		p2.extend([c2, c1])

while p1 and p2:
	turn(p1, p2)
	
winner = p1 if p1 else p2
N = len(winner)
score = sum((N-i)*c for (i,c) in enumerate(winner))
print("Part 1:", score)


def turn2(p1, p2):
	c1, c2 = p1.popleft(), p2.popleft()
	# check if we have enough cards to recurse
	if c1 <= len(p1) and c2 <= len(p2):
		p1sub, p2sub = deque(list(p1)[:c1]), deque(list(p2)[:c2])
		if play(p1sub, p2sub):
			p1.extend([c1, c2])
		else:
			p2.extend([c2, c1])
	else:
		if c1 > c2:
			p1.extend([c1, c2])
		else:
			p2.extend([c2, c1])

def play(p1, p2):
	# returns True if p1 wins
	h = tuple(p1) + (0,) + tuple(p2)
	seen = set([h])
	while True:
		turn2(p1, p2)
		if not p1:
			return False
		if not p2:
			return True
		h = tuple(p1) + (0,) + tuple(p1)
		if h in seen:
			return True
		else:
			seen.add(h)

p1, p2 = data.split("\n\n")
p1, p2 = [deque(int(s) for s in p.splitlines()[1:]) for p in [p1,p2]]
while p1 and p2:
	turn2(p1, p2)
	
winner = p1 if p1 else p2
N = len(winner)
score = sum((N-i)*c for (i,c) in enumerate(winner))
print("Part 2:", score)
