import os, sys
sys.path.append(os.path.realpath(".."))
from util import *
from queue import PriorityQueue
from collections import namedtuple

#test()
input = get_input()

Valve = namedtuple("Valve", "index name flow tunnels")

tmax = 30

start_index = -1

def parse_line(i, l):
	# Valve II has flow rate=0; tunnels lead to valves AA, JJ
	# Valve JJ has flow rate=21; tunnel leads to valve II
	res = parse("Valve {} has flow rate={:d}; {}", l)
	if not res:
		print("couldnt parse")
		print(l)
	tunnels = res[2].split(" ")[4:]
	tunnels = [t.strip(",") for t in tunnels]
	if res[0] == "AA":
		global start_index
		start_index = i
	return Valve(i, res[0], res[1], tunnels)


valves = [parse_line(i, l) for (i,l) in enumerate(input.splitlines())]
sorted_valves = sorted(valves, key=lambda v: v.flow, reverse=True)
valves_by_name = dict((v.name, v) for v in valves)

# closed is a bitset packed in int64
State = namedtuple("State", "score, time, cur, closed")

def bits_contains(s, b):
	return (1 << b) & s != 0

def best(s):
	total = s.score
	rem_time = tmax - s.time
	# may or may not be optimal to open current valve so for upper bound assume we do but dont count the time
	if bits_contains(s.closed, s.cur):
		total += valves[s.cur].flow * rem_time
	# upper bound on best score: open all remaining valves next
	rem = [v for v in sorted_valves if bits_contains(s.closed, v.index) and v.flow and v.index != s.cur]
	
	# how many more can we do? assume best case of one min to travel, one min to open for each
	rem = rem[:rem_time//2]
	total += sum(v.flow*(rem_time-(2*i+2)) for (i,v) in enumerate(rem))
	return total

def next_states(s):
	nxt = []
	cur_valve = valves[s.cur]
	if bits_contains(s.closed, s.cur) and cur_valve.flow:
		s2 = s._replace(
			time=s.time+1,
			score=s.score+cur_valve.flow*(tmax-1-s.time),
			closed=s.closed & ~(1<<s.cur)
			)
		nxt.append(s2)
	for n in cur_valve.tunnels:
		s2 = s._replace(
			time=s.time+1,
			cur=valves_by_name[n].index
			)
		nxt.append(s2)
	return nxt

init = State(0, 0, start_index, 2**len(valves)-1)

states = PriorityQueue()
states.put((0,init))

# maps (cur,closed) -> set{(score,time)}
seen = {(init.cur, init.closed): set([(0, 0)])}

best_score = -1
i = 0
skipped = 0
while not states.empty() and i < 1000000:
	i += 1
	sc, s = states.get()
	if s.score > best_score:
		best_score = s.score
	if s.time == tmax:
		continue
	if best(s) <= best_score:
		# ignore states whose best outcome cant beat the current best
		skipped += 1
		continue
	for s2 in next_states(s):
		k = (s2.cur, s2.closed)
		skip = False
		if k in seen:
			drop = []
			for (score, time) in seen[k]:
				if s2.time >= time and s2.score <= score:
					skip = True
				if time >= s2.time and score <= s2.score:
					drop.append((score, time))
			for pair in drop:
				seen[k].remove(pair)
		else:
			seen[k] = set()
		if not skip:
			seen[k].add((s2.score, s2.time))
			states.put((-best(s2), s2))


print("Part 1:", best_score)

tmax = 26

State2 = namedtuple("State2", "score, time, cur, cur2, closed")

def best2(s):
	total = s.score
	rem_time = tmax - s.time
	# may or may not be optimal to open current valve so for upper bound assume we do but dont count the time
	if bits_contains(s.closed, s.cur):
		total += valves[s.cur].flow * rem_time
	if bits_contains(s.closed, s.cur2) and s.cur != s.cur2:
		total += valves[s.cur2].flow * rem_time
	# upper bound on best score: open all remaining valves next
	rem = [v for v in sorted_valves if bits_contains(s.closed, v.index) and v.flow and v.index != s.cur and v.index != s.cur2]
	
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
		if bits_contains(s2.closed, s.cur2) and cur2_valve.flow:
			# stay and open
			s3 = s2._replace(
				score=s2.score+cur2_valve.flow*(tmax-1-s.time),
				closed=s2.closed & ~ (1<<s.cur2)
			)
			nxt.append(s3)
	# elephant moves
	for n in cur2_valve.tunnels:
		for s2 in your_moves:
			s3 = s2._replace(
				cur2=valves_by_name[n].index
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
	return nxt

init = State2(0, 0, start_index, start_index, 2**len(valves)-1)

states = PriorityQueue()
states.put((-best2(init),init))

# maps (cur,cur2,closed) -> set{(score,time)}
seen = {(init.cur, init.cur2, init.closed): set([(0, 0)])}

best_score = -1
i = 0
skipped = 0
while not states.empty() and i < 10000000:
	i += 1
	#if i % 100000 == 0:
		#print("step", i, states.qsize())
	sc, s = states.get()
	if s.score > best_score:
		best_score = s.score
	if s.time == tmax:
		continue
	for s2 in next_states2(s):
		best = best2(s2)
		if best <= best_score:
			# ignore states whose best outcome cant beat the current best
			skipped += 1
			continue
		
		k = (s2.cur, s2.cur2, s2.closed)
		skip = False
		if k in seen:
			drop = []
			for (score, time) in seen[k]:
				if s2.time >= time and s2.score <= score:
					skip = True
				if time >= s2.time and score <= s2.score:
					drop.append((score, time))
			for pair in drop:
				seen[k].remove(pair)
		else:
			seen[k] = set()
		if not skip:
			seen[k].add((s2.score, s2.time))
			
			# going in order of score uses more steps but keeps fewer states in the queue
			#states.put((-s2.score, s2))
			states.put((-best, s2))


print("Part 2:", best_score)
