from parse import parse
from copy import copy
from collections import namedtuple
from queue import PriorityQueue
from time import time
import math

input = open("input_test.py").read()

class Blueprint (object):
	def __init__(self, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geo_ore_cost, geo_obs_cost):
		self.ore_cost = ore_cost
		self.clay_cost = clay_cost
		self.obs_ore_cost = obs_ore_cost
		self.obs_clay_cost = obs_clay_cost
		self.geo_ore_cost = geo_ore_cost
		self.geo_obs_cost = geo_obs_cost

class StateOld(object):
	def __init__(self):
		self.ore = 0
		self.clay = 0
		self.obsidian = 0
		self.geode = 0
		self.ore_bot = 1
		self.clay_bot = 0
		self.obs_bot = 0
		self.geo_bot = 0
	
	def __str__(self):
		return "O/C/O/G: {}/{}/{}/{} -- Bots: {}/{}/{}/{}".format(self.ore, self.clay, self.obsidian, self.geode, self.ore_bot, self.clay_bot, self.obs_bot, self.geo_bot)
	
	def __repr__(self):
		return str(self)
	
	def __hash__(self):
		return hash(self.tuple())
	
	def __eq__(self, s):
		return self.tuple() == s.tuple()
		
	def tuple(self):
		return (self.ore, self.clay, self.obsidian, self.geode, self.ore_bot, self.clay_bot, self.obs_bot, self.geo_bot)
	
	def better(self, s2):
		# s2 is better
		t1, t2 = self.tuple(), s2.tuple()
		return all(a<=b for (a,b) in zip(t1, t2))

State = namedtuple("State", "ore clay obsidian geode ore_bot clay_bot obs_bot geo_bot")

def new_state():
	return State(0,0,0,0,1,0,0,0)

def better(s1, s2):
		# s2 is better
		#return all(a<=b for (a,b) in zip(s1, s2))
		return (
			s1[0] <= s2[0] and
			s1[4] <= s2[4] and
			s1[1] <= s2[1] and
			s1[5] <= s2[5] and
			s1[2] <= s2[2] and
			s1[6] <= s2[6] and
			s1[3] <= s2[3] and
			s1[7] <= s2[7]
		)

def state_str(s):
		#return "O/C/O/G: {}/{}/{}/{} -- Bots: {}/{}/{}/{}".format(s.ore, s.clay, s.obsidian, s.geode, s.ore_bot, s.clay_bot, s.obs_bot, s.geo_bot)
		return "{}/{}/{}/{}:{}/{}/{}/{}".format(s.ore, s.clay, s.obsidian, s.geode, s.ore_bot, s.clay_bot, s.obs_bot, s.geo_bot)

def parse_line(l):
	# Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
	r = parse("Blueprint {}: Each ore robot costs {:d} ore. Each clay robot costs {:d} ore. Each obsidian robot costs {:d} ore and {:d} clay. Each geode robot costs {:d} ore and {:d} obsidian.", l)
	return Blueprint(*[r[i] for i in range(1,7)])

blueprints = [parse_line(l) for l in input.splitlines() if l]

def incr_old(s):
	s2 = copy(s)
	s2.ore = s.ore + s.ore_bot
	s2.clay = s.clay + s.clay_bot
	s2.obsidian = s.obsidian + s.obs_bot
	s2.geode = s.geode + s.geo_bot
	return s2
	
def next_states_old(s, b):
	ss = []
	# just sit
	s2 = incr(s)
	ss.append(s2)
	
	# ore bot
	if s.ore >= b.ore_cost:
		s3 = copy(s2)
		s3.ore -= b.ore_cost
		s3.ore_bot += 1
		ss.append(s3)
	
	# clay bot
	if s.ore >= b.clay_cost:
		s3 = copy(s2)
		s3.ore -= b.clay_cost
		s3.clay_bot += 1
		ss.append(s3)
	
	# obsidian bot
	if s.ore >= b.obs_ore_cost and s.clay >= b.obs_clay_cost:
		s3 = copy(s2)
		s3.ore -= b.obs_ore_cost
		s3.clay -= b.obs_clay_cost
		s3.obs_bot += 1
		ss.append(s3)
	
	# geode bot
	if s.ore >= b.geo_ore_cost and s.obsidian >= b.geo_obs_cost:
		s3 = copy(s2)
		s3.ore -= b.geo_ore_cost
		s3.obsidian -= b.geo_obs_cost
		s3.geo_bot += 1
		ss.append(s3)
	
	return ss

def incr(s):
	return s._replace(
		ore=s.ore+s.ore_bot,
		clay=s.clay+s.clay_bot,
		obsidian=s.obsidian+s.obs_bot,
		geode=s.geode+s.geo_bot,
	)
	
def next_states(s, b):
	ss = []
	# just sit
	s2 = incr(s)
	ss.append(s2)
	
	# ore bot
	if s.ore >= b.ore_cost:
		s3 = s2._replace(
			ore=s2.ore-b.ore_cost,
			ore_bot=s2.ore_bot+1
			)
		ss.append(s3)
	
	# clay bot
	if s.ore >= b.clay_cost:
		s3 = s2._replace(
			ore=s2.ore-b.clay_cost,
			clay_bot=s2.clay_bot+1
		)
		ss.append(s3)
	
	# obsidian bot
	if s.ore >= b.obs_ore_cost and s.clay >= b.obs_clay_cost:
		s3 = s2._replace(
			ore=s2.ore-b.obs_ore_cost,
			clay=s2.clay-b.obs_clay_cost,
			obs_bot=s2.obs_bot+1
		)
		ss.append(s3)
	
	# geode bot
	if s.ore >= b.geo_ore_cost and s.obsidian >= b.geo_obs_cost:
		s3 = s2._replace(
			ore=s2.ore-b.geo_ore_cost,
			obsidian=s2.obsidian-b.geo_obs_cost,
			geo_bot=s2.geo_bot+1
		)
		ss.append(s3)
	
	return set(ss)

def score(s, b):
	# (g', g'', g''')  packed as g' << 16 + g'' << 8 + g'''
	gdot = s.geo_bot
	gdotdot = min(s.ore_bot/b.geo_ore_cost, s.obs_bot/b.geo_obs_cost)
	# approx: only include the b'' term in g'''
	gdotdotdot = min(s.ore_bot/b.obs_ore_cost, s.clay_bot/b.obs_clay_cost)
	return -1 * (gdot * (1<<16) + gdotdot * (1<<8) + gdotdotdot)

def score_dumb(s, b, t):
	# roughly, g' * trem + (1/2)g'' * trem^2 + (1/6)g''' * trem^3
	gdot = s.geo_bot
	gdotdot = min(s.ore_bot/b.geo_ore_cost, s.obs_bot/b.geo_obs_cost)
	# approx: only include the b'' term in g'''
	gdotdotdot = min(s.ore_bot/b.obs_ore_cost, s.clay_bot/b.obs_clay_cost)
	trem = 24 - t
	return -1 * ((gdot * trem) + (gdotdot * .5 * trem**2)  + (gdotdotdot * trem**3 / 6))

def constraints(max_geo, bp):
	tg = math.floor(24.5 - .5 * math.sqrt(1+8*max_geo))
	tb = math.floor(tg - .5 - .5 * math.sqrt(1+8*bp.geo_obs_cost))
	tc = math.floor(tb - .5 - .5 * math.sqrt(1+8*bp.obs_clay_cost))
	return tg, tb, tc
	
bp = blueprints[1]

start = new_state()
states = PriorityQueue()

t,s = 0, start
states.put((t, score(s, bp), s))
state_sets = dict((i,set()) for i in range(25))
state_sets[t].add(s)

max_geo = 0
tg, tb, tc = constraints(0, bp)

i = 0
t1 = time()
while not states.empty(): # and i < 1000000:
	i += 1
	negt, _, s = states.get()
	t = -negt + 1
	if i % 10000 == 0:
		print("checking", i, state_str(s))
	if t == 24:
		s = incr(s) # final harvest
		if s.geode > max_geo:
			max_geo = s.geode
			tg, tb, tc = constraints(max_geo, bp)
			print("new best:", state_str(s), tg,tb,tc)
			if max_geo == 9:
				t2 = time()
				print("time", t2-t1)
				#break
		continue
		
	# check some cases where we can rule this state out
	# bp0: 20,15,10
	# bp1: 20,14,9
	if s.geo_bot == 0 and t > tg:
		continue
	if s.obs_bot == 0 and t > tb:
		continue
	if s.clay_bot == 0 and t > tc:
		continue
	
	nn = next_states(s, bp)
	checked = state_sets[t]
	for n in nn:
		#if not(n in checked or any(better(n, s2) for s2 in checked)):
		if not n in checked:
			#print("adding {:.2f}: {}".format(score(n, blueprints[0], t+1), state_str(n)))
			states.put((-t, score(n, bp), n))
			checked.add(n)
	#print()

"""
for i in range(24):
	t1 = time()
	nxt = set()
	for s in states:
		nxtnxt = nxt.union(next_states(s, blueprints[0]))
		#nxt = set(filter(lambda s: not any(s is not s2 and better(s, s2) for s2 in nxtnxt), nxtnxt))
		nxt = nxtnxt
	t2 = time()
	print("finding next:", t2-t1)
	
	nxts = sorted(nxt)
	nxt = []
	for j,s in enumerate(nxts):
		if not any(s != s2 and better(s, s2) for s2 in nxts[j:]):
			nxt.append(s)
		
	#states = list(filter(lambda s: not any(s is not s2 and better(s, s2) for s2 in nxt), nxt))
	states = nxt
	
	t3 = time()
	print("filtering:", t3-t2)
	print()
	print("step", i, len(states), "states")
	#for s in states:
	#	print(state_str(s))
"""

print(max_geo)
t3 = time()
print("full time", t3-t1)

#print(max(s.geode for s in states))
