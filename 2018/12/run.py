initial = ".##.##...#.###..#.#..##..###..##...####.#...#.##....##.#.#...#...###.........##...###.....##.##.##"

fmt = "{} => {}"

vals = [1 if c == '#' else 0 for c in initial]
first_val = 1+100
last_val = 97+100
vals = [0]*100 + vals + [0]*100
offset = 100

def code(digs):
	return sum(x*2**i for (i,x) in enumerate(digs))

def code_str(s):
	digs = [1 if c == '#' else 0 for c in s]
	return code(digs)
	
from parse import parse
input = open("input.txt").readlines()
rules = [parse(fmt,l) for l in input]
rules_by_code = [0]*32
for r in rules:
	c = code_str(r[0])
	rules_by_code[c] = 1 if r[1] == '#' else 0

print(rules_by_code)

old_vals = vals[:]

escapees = []

def do_step(n):
	global first_val, last_val, old_vals, vals
	if vals[0] == 1 or vals[1] == 1 or vals[-1] == 1 or vals[-2] == 1:
		print("not enough offset!", n)
		raise Exception("offset insufficient")
	old_vals = vals[:]
	for i in range(len(vals)):
		state = old_vals[i-2:i+3]
		nxt = rules_by_code[code(state)]
		if nxt == 1:
			if i < first_val:
				first_val = i
			elif i > last_val:
				# escapes?
				if vals[i-1] == 0 and vals[i-2] == 0:
					escapees.append([i, n])
					nxt = 0
				else:
					last_val = i
					
		vals[i] = nxt 

def show():
	print("".join([".","#"][x] for x in vals))

show()
for i in range(1,200):
	do_step(i)

show()
print(sum(i-offset for i in range(len(vals)) if vals[i] == 1))
print(escapees)

def escapee_value(e):
	return(e[0]-offset + (50000000000-e[1]))
	
print(sum(escapee_value(e) for e in escapees))
