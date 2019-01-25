class State (object):
	A = 1
	B = 2
	C = 3
	D = 4
	E = 5
	F = 6
	

rules = {
	State.A: {
		"write": [1, 1],
		"move": [1, -1],
		"next": [State.B, State.E],
	},
	State.B: {
		"write": [1, 1],
		"move": [1, 1],
		"next": [State.C, State.F],
	},
	State.C: {
		"write": [1, 0],
		"move": [-1, 1],
		"next": [State.D, State.B],
	},
	State.D: {
		"write": [1, 0],
		"move": [1, -1],
		"next": [State.E, State.C],
	},
	State.E: {
		"write": [1, 0],
		"move": [-1, 1],
		"next": [State.A, State.D],
	},
	State.F: {
		"write": [1, 1],
		"move": [1, 1],
		"next": [State.A, State.C],
	},
}

class Machine (object):
	def __init__(self):
		self.tape = [0]
		self.loc = 0
		self.state = State.A
	
	def step(self):
		cur = self.tape[self.loc]
		rule = rules[self.state]
		self.tape[self.loc] = rule["write"][cur]
		self.loc += rule["move"][cur]
		self.state = rule["next"][cur]
		# adjust buffer if necessary
		tape_len = len(self.tape)
		if self.loc >= tape_len:
			self.tape += [0 for i in range(tape_len)]
		elif self.loc == -1:
			self.tape = [0 for i in range(tape_len)] + self.tape
			self.loc += tape_len

m = Machine()
for i in range(12523873):
	m.step()

print(sum(m.tape))
