from me import *
from sickos.yes import *

input = get_data_2023(7)

input = input_test

# Part A

ranks = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}

def rank(c):
	return ranks[c] if c in ranks else int(c)

# Returns a list of rank cardinalities in descending order
# Eg, a full house is [3, 2]
def score(hand):
	return pipeline(hand) | set | [hand.count] | sorted	| reversed | list | DONE

resultA = (pipeline(input.splitlines())
	| [str.strip]
	| [(str.split, " ")]
	| [lambda h,b: (score(h), lmap(rank, h), int(b), h)]
	| sorted
	| enumerate
	| [lambda i, h: (i+1)*h[2]]
	| sum
	| DONE
)
	

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=7)

# Part B

def rankB(c):
	return 1 if c == "J" else (ranks[c] if c in ranks else int(c))
	
def scoreB(hand):
	"""Same as above, but remove the jokers and add that many to the highest group"""
	joks = hand.count("J")
	if joks == 5:
		return [5]
	return (pipeline(hand)
		| (str.replace, "J", "")
		| set | [hand.count] | sorted | reversed | list
		| (lambda l: [l[0]+joks] + l[1:])
		| DONE
	)
	
resultB = (pipeline(input.splitlines())
	| [str.strip]
	| [(str.split, " ")]
	| [lambda h,b: (scoreB(h), lmap(rankB, h), int(b), h)]
	| sorted
	| enumerate
	| [lambda i, h: (i+1)*h[2]]
	| sum
	| DONE
)

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=7)
