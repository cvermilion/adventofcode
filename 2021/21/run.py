p1 = 9
score1 = 0
p2 = 10
score2 = 0
turn = 1
die = 0
rolls = 0

while score1 < 1000 and score2 < 1000:
	move = (3 * die + 3) % 100 + 3
	die = (die + 2) % 100 + 1
	if turn == 1:
		p1 = (p1 + move - 1) % 10 + 1
		score1 += p1
		turn = 2
	else:
		p2 = (p2 + move - 1) % 10 + 1
		score2 += p2
		turn = 1
	rolls += 3

print("Part 1:", rolls*min([score1, score2])))

# all possible rolls and their weights
rolls = [0 for i in range(10)]
for i in range(1,4):
	for j in range(1,4):
		for k in range(1,4):
			rolls[i+j+k] += 1

p1 = 9
p2 = 10
# The full state of a game is just each position and each score (and whose turn it is).
# We just count the number in each state after each turn, removing the states where
# someone has won.
p1states = {(p1, p2, 0, 0): 1}
p2states = {}
p1wins = 0
p2wins = 0
while p1states:
    # ready player one
	for ((p1,p2,score1,score2), cnt) in p1states.items():
		for r in range(3, 10):
			weight = rolls[r]
			p1next = (p1 + r - 1) % 10 + 1
			score1next = score1 + p1next
			if score1next >= 21:
				p1wins += weight * cnt
			else:
				state = (p1next,p2,score1next,score2)
				p2states[state] = p2states.get(state, 0) + weight * cnt
	p1states = {}
	
    # player two 
	for ((p1,p2,score1,score2), cnt) in p2states.items():
		for r in range(3, 10):
			weight = rolls[r]
			p2next = (p2 + r - 1) % 10 + 1
			score2next = score2 + p2next
			if score2next >= 21:
				p2wins += weight * cnt
			else:
				state = (p1,p2next,score1,score2next)
				p1states[state] = p1states.get(state, 0) + weight * cnt
	p2states = {}

print("Part 2:", max([p1wins, p2wins]))
