input_test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

def score(c):
	x = ord(c)
	if x > 95:
		return x - 96
	return x - 64 + 26

#input = input_test.splitlines()

input = open("input.py").readlines()

lines = [list(l.strip()) for l in input]
items = [(set(l[:int(len(l)/2)]), set(l[int(len(l)/2):])) for l in lines]
overlap = [a.intersection(b).pop() for (a,b) in items]

print(sum(map(score, overlap)))

groups = [(set(lines[3*i]), set(lines[3*i+1]), set(lines[3*i+2])) for i in range(int(len(lines)/3))]

badges = [a.intersection(b).intersection(c).pop() for (a,b,c) in groups]

print(sum(map(score, badges)))
