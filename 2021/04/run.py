import functools
import operator

data = open("input.txt").read().splitlines()
calls = [int(n) for n in data[0].split(",")]

boards = [[int(n) for n in b.split()] for b in "\n".join(data[2:]).split("\n\n")]

square_ids = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

# map of number to square_id for each board
board_placements = [dict((n,square_ids[i]) for (i,n) in enumerate(b)) for b in boards]

def score(board_placement, calls):
    return functools.reduce(operator.mul, [board_placement.get(n, 1) for n in calls])

rows = [[square_ids[5*r + c] for c in range(5)] for r in range(5)]
cols = [[square_ids[5*r + c] for r in range(5)] for c in range(5)]
winning_scores = [functools.reduce(operator.mul, l) for l in rows + cols]
print(winning_scores)

winner = None
winning_step = None
for step in range(1, len(calls)+1):
    scores = [score(b, calls[:step]) for b in board_placements]
    wins = [any(s%w == 0 for w in winning_scores) for s in scores]
    if any(wins):
        winner = [i for (i,w) in enumerate(wins) if w][0]
        winning_step = step
        break

winner_score = sum(k for k in boards[winner] if k not in calls[:winning_step]) * calls[winning_step-1]

print("Part 1:", winner_score)

# Now find the *last* winner
last_winner = None
last_winning_step = None
for step in range(1, len(calls)+1):
    scores = [score(b, calls[:step]) for b in board_placements]
    wins = [any(s%w == 0 for w in winning_scores) for s in scores]
    if len([w for w in wins if not w]) == 1:
        last_winner = [i for (i,w) in enumerate(wins) if not w][0]
    if len([w for w in wins if not w]) == 0:
        last_winning_step = step
        break

last_winner_score = sum(k for k in boards[last_winner] if k not in calls[:last_winning_step]) * calls[last_winning_step-1]

print("Part 2:", last_winner_score)
