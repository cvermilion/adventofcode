from parse import parse
from copy import copy
from collections import namedtuple
from queue import PriorityQueue
from time import time
import math
import operator
import functools

input = open("input.py").read()

class Blueprint (object):
	def __init__(self, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geo_ore_cost, geo_obs_cost):
		self.ore_cost = ore_cost
		self.clay_cost = clay_cost
		self.obs_ore_cost = obs_ore_cost
		self.obs_clay_cost = obs_clay_cost
		self.geo_ore_cost = geo_ore_cost
		self.geo_obs_cost = geo_obs_cost

State = namedtuple("State", "ore clay obsidian geode ore_bot clay_bot obs_bot geo_bot")

def new_state():
	return State(0,0,0,0,1,0,0,0)

def state_hash(s):
	return s.ore | s.ore_bot << 8 | s.clay << 16 | s.clay_bot << 24 | s.obsidian << 32 | s.obs_bot << 40 | s.geode << 48 | s.geo_bot << 56

def better_hash(h1, h2):
	return all(b1 <= b2 for (b1, b2) in zip(h1.to_bytes(8, "little"), h2.to_bytes(8, "little")))

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
	gdotdot = min(1, s.ore_bot/b.geo_ore_cost, s.obs_bot/b.geo_obs_cost)
	gdotdotdot = min(
		min(1, s.ore_bot/b.obs_ore_cost)/b.geo_obs_cost,
		min(1, s.clay_bot/b.obs_clay_cost)/b.geo_obs_cost,
		min(1, s.ore_bot/b.ore_cost)/b.geo_ore_cost
	)
	return -1 * (gdot * (1<<16) + gdotdot * (1<<8) + gdotdotdot)

def score2(s, b):
	# (g', g'', g''')  packed as g' << 16 + g'' << 8 + g'''
	# count progress toward bots
	# but this has worse perf for some reason?
	gp = s.geo_bot + min(1, s.ore/b.geo_ore_cost, s.obsidian/b.geo_obs_cost)
	op = s.ore_bot + min(1, s.ore/b.ore_cost)
	bp = s.obs_bot + min(1, s.ore/b.obs_ore_cost, s.clay/b.obs_clay_cost)
	cp = s.clay_bot + min(1, s.ore/b.clay_cost)
	
	gdot = gp
	gdotdot = min(1, op/b.geo_ore_cost, bp/b.geo_obs_cost)
	gdotdotdot = min(
		min(1, op/b.obs_ore_cost)/b.geo_obs_cost,
		min(1, cp/b.obs_clay_cost)/b.geo_obs_cost,
		min(1, op/b.ore_cost)/b.geo_ore_cost
		)
	return -1 * (gdot * (1<<16) + gdotdot * (1<<8) + gdotdotdot)

def constraints(tmax, max_geo, bp):
	tg = math.floor(tmax + .5 - .5 * math.sqrt(1+8*max_geo))
	tb = math.floor(tg - .5 - .5 * math.sqrt(1+8*bp.geo_obs_cost))
	tc = math.floor(tb - .5 - .5 * math.sqrt(1+8*bp.obs_clay_cost))
	return tg, tb, tc

def max_possible_geode(dt, s):
	# make sure to count the final increment
	return s.geode + s.geo_bot*(dt+1) + .5*dt*(dt+1)

def max_possible_obs(dt, s):
	return s.obsidian + s.obs_bot*dt + .5*dt*(dt+1)

def max_possible_clay(dt, s):
	return s.clay + s.clay_bot*dt + 5*dt*(dt+1)


def max_geo(tmax, bp, do_recurse=False, verbose=False):
	if tmax <= 1:
		return new_state()
	
	t1 = time()
	
	# use one-step shorter solution as a lower bound
	best = new_state()
	if do_recurse:
		best_prev = max_geo(tmax-1, bp, do_recurse, verbose)
		nxt = next_states(best_prev, bp)
		best = nxt.pop()
		for n in nxt:
			if n.geode > best.geode:
				best = n
	
		print()
		print("tmax:", tmax)
		print("best for", tmax-1, best.geode)
		
	start = new_state()
	states = PriorityQueue()
	
	t,s = 0, start
	states.put((t, score(s, bp), s))
	state_sets = dict((i,set()) for i in range(tmax+1))
	state_sets[t].add(s)
	
	tg, tb, tc = constraints(tmax, best.geode, bp)
	
	i = 0
	while not states.empty():
		i += 1
		negt, _, s = states.get()
		t = -negt + 1
		if verbose and i % 100000 == 0:
			print("checking {} ({},{}) {}".format(i, tmax, best.geode, state_str(s)))
		if t == tmax:
			s = incr(s) # final harvest
			if (s.geode > best.geode) or (s.geode == best.geode and s.geo_bot > best.geo_bot):
				best = s
				tg, tb, tc = constraints(tmax, best.geode, bp)
				if verbose:
					print("new best:", state_str(s), tg,tb,tc)
			continue
			
		# check some cases where we can rule this state out
		if t >= tg and max_possible_geode(tmax-t, s) < best.geode:
			# assuming we could build geo bots every minute could we beat the best
			continue
		if t >= tb and s.geo_bot == 0 and max_possible_obs(tg-t, s) < bp.geo_obs_cost:
			# if no geode bots, so we have time to build enough obsidian to switch to geode bots by tg
			continue
		if s.obs_bot == 0 and t >= tc and max_possible_clay(tb-t, s) < bp.obs_clay_cost:
			continue
		
		nn = next_states(s, bp)
		checked = state_sets[t]
		for n in nn:
			if not n in checked:
				states.put((-t, score(n, bp), n))
				checked.add(n)
	
	t3 = time()
	if verbose:
		print("full time", t3-t1)
	return best


# Part 1
t1 = time()

quality_nums = []
for (ii, bp) in enumerate(blueprints):
	id = ii+1
	quality_nums.append(max_geo(24, bp).geode * id)
	
print("Part 1:", sum(quality_nums))

max_geodes = []
for (id, bp) in enumerate(blueprints[:3]):
	print()
	print("BP", id, "******")
	print()

	max_geodes.append(max_geo(32, bp, do_recurse=True, verbose=True).geode)
	
print("Part 2:", functools.reduce(operator.mul, max_geodes))

t2 = time()
print("Total time:", t2-t1)
