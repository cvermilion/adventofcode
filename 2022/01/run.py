test_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

input=test_input

input = open("input.py").read()

elves = input.split("\n\n")
cals = [[int(c) for c in e.splitlines()] for e in elves]

totals = [sum(cs) for cs in cals]

print(max(totals))

ordered = list(reversed(sorted(totals)))
print(sum(ordered[:3]))
