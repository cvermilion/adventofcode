from parse import parse
from queue import PriorityQueue
from collections import namedtuple

input = open("input.py").read()

Valve = namedtuple("Valve", "name flow tunnels")

tmax = 26

def parse_line(l):
	# Valve II has flow rate=0; tunnels lead to valves AA, JJ
	# Valve JJ has flow rate=21; tunnel leads to valve II
	res = parse("Valve {} has flow rate={:d}; {}", l)
	if not res:
		print("couldnt parse")
		print(l)
	tunnels = res[2].split(" ")[4:]
	tunnels = [t.strip(",") for t in tunnels]
	return Valve(res[0], res[1], tunnels)

valves = [parse_line(l) for l in input.splitlines()]
sorted_valves = sorted(valves, key=lambda v: v.flow, reverse=True)
valves = dict((v.name, v) for v in valves)

State = namedtuple("State", "score, time, cur, closed")

def best(s):
	total = s.score
	rem_time = tmax - s.time
	# may or may not be optimal to open current valve so for upper bound assume we do but dont count the time
	if s.cur in s.closed:
		total += valves[s.cur].flow * rem_time
	# upper bound on best score: open all remaining valves next
	rem = [v for v in sorted_valves if v.name in s.closed and v.flow and v.name != s.cur]
	
	# how many more can we do? assume best case of one min to travel, one min to open for each
	rem = rem[:rem_time//2]
	total += sum(v.flow*(rem_time-(2*i+2)) for (i,v) in enumerate(rem))
	return total

def next_states(s):
	nxt = []
	cur_valve = valves[s.cur]
	if s.cur in s.closed and cur_valve.flow:
		s2 = s._replace(
			time=s.time+1,
			score=s.score+cur_valve.flow*(tmax-1-s.time),
			closed=s.closed.difference(set([s.cur]))
			)
		nxt.append(s2)
	for n in cur_valve.tunnels:
		s2 = s._replace(
			time=s.time+1,
			cur=n
			)
		nxt.append(s2)
	#print("next")
	#print(nxt)
	return nxt

init = State(0, 0, "AA", set(valves.keys()))

#init = init._replace(best=best(init))

states = PriorityQueue()
states.put((0,init))

best_score = -1
i = 0
skipped = 0
while not states.empty() and i < 0:
	i += 1
	sc, s = states.get()
	if s.score > best_score:
		print("checking", best_score, sc, s)
		best_score = s.score
	if s.time == tmax:
		if s.score > best_score:
			best_score = s.score
		continue
	if best(s) <= best_score:
		# ignore states whose best outcome cant beat the current best
		skipped += 1
		continue
	for s2 in next_states(s):
		states.put((-s2.score, s2))
		#states.put((-best(s2), s2))


print(i, skipped, best_score)

# part 2

State2 = namedtuple("State2", "score, time, cur, cur2, closed")

def best2(s):
	total = s.score
	rem_time = tmax - s.time
	# may or may not be optimal to open current valve so for upper bound assume we do but dont count the time
	if s.cur in s.closed:
		total += valves[s.cur].flow * rem_time
	if s.cur2 in s.closed and s.cur != s.cur2:
		total += valves[s.cur2].flow * rem_time
	# upper bound on best score: open all remaining valves next
	rem = [v for v in sorted_valves if v.name in s.closed and v.flow and v.name != s.cur and v.name != s.cur2]
	
	# how many more can we do? assume best case of one min to travel, one min to open for each
	rem = rem[:2*(rem_time//2)]
	total += sum(v.flow*(rem_time-(2*(i//2)+2)) for (i,v) in enumerate(rem))
	return total

def next_states2(s):
	nxt = []
	your_moves = next_states(s)
	cur_valve = valves[s.cur]
	cur2_valve = valves[s.cur2]
	for s2 in your_moves:
		if s.cur2 in s2.closed and cur2_valve.flow:
			# stay and open
			s3 = s2._replace(
				score=s2.score+cur2_valve.flow*(tmax-1-s.time),
				closed=s2.closed.difference(set([s.cur2]))
			)
			nxt.append(s3)
	# elephant moves
	for n in cur2_valve.tunnels:
		for s2 in your_moves:
			s3 = s2._replace(
				cur2=n
			)
			nxt.append(s3)
	
	# doesnt matter if im at X and elephant is at Y or vice versa; put in order and let set dedupe
	nxt = [(n if n.cur <= n.cur2 else
		n._replace(cur=n.cur2, cur2=n.cur))
		for n in nxt]
	
	dupes = set()
	for i,n in enumerate(nxt):
		for j in range(i+1, len(nxt)):
			if n == nxt[j]:
				dupes.add(j)
	nxt = [n for (i,n) in enumerate(nxt) if i not in dupes]
	
	#print("next")
	#print(nxt)
	return nxt

init = State2(0, 0, "AA", "AA", set(valves.keys()))

#init = init._replace(best=best(init))

states = PriorityQueue()
states.put((-best2(init),init))

best_score = -1
i = 0
skipped = 0
while not states.empty() and i < 1000:
	i += 1
	if i % 100000 == 0:
		print("step", i, states.qsize())
	sc, s = states.get()
	#print("checking", best_score, sc, s)
	if s.score > best_score:
		#print("checking", best_score, sc, s)
		best_score = s.score
	if s.time == tmax:
		#if s.score > best_score:
		#	best_score = s.score
		continue
	for s2 in next_states2(s):
		best = best2(s2)
		if best <= best_score:
			# ignore states whose best outcome cant beat the current best
			skipped += 1
			continue
		#states.put((-s2.score, s2))
		states.put((-best, s2))


print(i, skipped, best_score)
