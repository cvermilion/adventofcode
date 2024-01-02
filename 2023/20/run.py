from me import *
from sickos.yes import *
from collections import namedtuple
from queue import SimpleQueue

input = get_data_2023(20)

#input = input_test

input_test_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
#input = input_test_2

FF = namedtuple("FF", ["name", "state", "outputs"])
And = namedtuple("And", ["name", "state", "outputs"])
Broadcaster = namedtuple("Broadcaster", ["name", "state", "outputs"])
Output = namedtuple("Output", ["name", "state", "outputs"])

Low, High = 0, 1
Off, On = 0, 1

# Part A

"""
broadcaster -> a, b, c
%a -> b
&inv -> a
"""
def parse_line(l):
	name, outs = l.split(" -> ")
	outs = outs.strip().split(", ")
	match name[0]:
		case "%":
			return FF(name[1:], {0: Off}, outs)
		case "&":
			return And(name[1:], {}, outs)
		case "b":
			return Broadcaster(name, {0: Low}, outs)
		case _:
			assert(False)

lines = lmap(parse_line, input.splitlines())
gates = dict((g.name, g) for g in lines)
gates["output"] = Output("output", Low, [])
gates["rx"] = Output("rx", Low, [])

for (name, g) in gates.items():
	for o in g.outputs:
		if o in gates:
			match gates[o]:
				case And(state=d):
					d[name] = Low

def do_pulse(pulses):
	src, dst, val = pulses.get()
	match gates[dst]:
		case Broadcaster() as b:
			b.state[0] = val
			for o in b.outputs:
				pulses.put((dst, o, val))
		case FF() as f:
			if val == Low:
				f.state[0], out = (Off, Low) if f.state[0] == On else (On, High)
				for o in f.outputs:
					pulses.put((dst, o, out))
		case And() as a:
			a.state[src] = val
			out = Low if all(a.state.values()) else High
			for o in a.outputs:
				pulses.put((dst, o, out))
	return val
				
sent = [0,0]
pulses = SimpleQueue()
for i in range(1000):
	delta = [0,0]
	pulses.put(("x", "broadcaster", Low))
	while not pulses.empty():
		val = do_pulse(pulses)
		delta[val] += 1
	
	sent[0] += delta[0]
	sent[1] += delta[1]
			
resultA = product(sent)

print("Part A:", resultA)
#aocd.submit(resultA, part="a", day=20)

# Part B

lines = lmap(parse_line, input.splitlines())
gates = dict((g.name, g) for g in lines)
gates["output"] = Output("output", Low, [])
gates["rx"] = Output("rx", Low, [])

for (name, g) in gates.items():
	for o in g.outputs:
		if o in gates:
			match gates[o]:
				case And(state=d):
					d[name] = Low

def do_pulse(pulses):
	src, dst, val = pulses.get()
	match gates[dst]:
		case Broadcaster() as b:
			b.state[0] = val
			for o in b.outputs:
				pulses.put((dst, o, val))
		case FF() as f:
			if val == Low:
				f.state[0], out = (Off, Low) if f.state[0] == On else (On, High)
				for o in f.outputs:
					pulses.put((dst, o, out))
		case And() as a:
			a.state[src] = val
			out = Low if all(a.state.values()) else High
			for o in a.outputs:
				pulses.put((dst, o, out))
	return src, dst, val
	
# each of these joins 12 bits (flip flops)
# the bits increment up to some N and then reset; the accumulator pulses low at N steps
accumulators = ["nx", "dj", "bz", "zp"]
invs = ["bh", "dl", "vd", "ns"]
bits = dict((a, set(g for g in list(gates[a].state.keys()) + gates[a].outputs if g not in invs)) for a in accumulators)
periods = {}

# vd, ns, bh, dl -> zh
# Find the period for each of these counters
pulses = SimpleQueue()
for i in range(10000):
	pulses.put(("x", "broadcaster", Low))
	while not pulses.empty():
		src, dst, val = do_pulse(pulses)
	for acc, bb in bits.items():
		if all(gates[b].state[0] == Off for b in bb):
			periods[acc] = i+1
	if len(periods) == 4:
		break

resultB = product(periods.values())

print("Part B:", resultB)
#aocd.submit(resultB, part="b", day=20)
