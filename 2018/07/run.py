from parse import parse
input = open("input.txt").readlines()
fmt = "Step {} must be finished before step {} can begin."
pairs = [parse(fmt, l) for l in input]

all_steps = set(p[0] for p in pairs).union(set(p[1] for p in pairs))

deps = dict((s, set()) for s in all_steps)
for p in pairs:
	dep, step = p[0], p[1]
	deps[step].add(dep)

#print(deps)
"""
out = []
ready = set()
while len(deps) > 0:
	ready = ready.union(set(s for (s,d) in deps.items() if len(d)==0))
	
	#print("ready:", ready)
	#print("all:", deps.keys())
	
	next = sorted(ready)[0]
	out.append(next)
	ready.remove(next)
	for d in deps.values():
		d.difference_update(set([next]))
	del deps[next]

print("".join(out))
"""

time = 0
ready = set()
active = []
while len(deps) > 0 or len(active) > 0:
	ready = ready.union(set(s for (s,d) in deps.items() if len(d)==0))
	
	while len(active) < 5 and len(ready) > 0:
		next = sorted(ready)[0]
		ready.remove(next)
		active.append([next, 60 + ord(next) - 64])
		del deps[next]
	
	for i in range(len(active)):
		active[i][1] = active[i][1] - 1
		if active[i][1] == 0:
			for d in deps.values():
				d.difference_update(set([active[i][0]]))
		
	active = [a for a in active if a[1] > 0]
	time += 1

print(time)
	
	
