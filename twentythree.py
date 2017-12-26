# 16 instructions, 68845613 executions
# 4 registers
text1="""set a 105700
set b 2
set c a
mod c b
jnz c 3
sub h -1
jnz 1 5
sub b -1
set c a
sub c b
jgz c -8
sub a -17
set c a
sub c 122700
jgz c 2
jnz 1 -14
"""

# count attempted divisors by 2
# 18 instructions, 39347886 executions
# 5 registers
text2="""set a 105700
set d -1
set b 2
set c a
mod c b
jnz c 3
sub h -1
jnz 1 6
sub b d
set d -2
set c a
sub c b
jgz c -9
sub a -17
set c a
sub c 122700
jgz c 2
jnz 1 -16
"""

# cut off prime check at sqrt(n)
# 20 instructions, 214256 executions
text="""set a 105700
set d -1
set b 2
set c a
mod c b
jnz c 3
sub h -1
jnz 1 8
sub b d
set d -2
set c b
mul c b
sub c a
jgz c 2
jnz 1 -11
sub a -17
set c a
sub c 122700
jgz c 2
jnz 1 -18
"""

def getr(regs, name):
	return regs.get(name, 0)

def setr(regs, name, val):
	regs[name] = val

def val(regs, y):
	try:
		return int(y)
	except:
		return getr(regs, y)

def set(regs, x, y):
	setr(regs, x, val(regs, y))

def sub(regs, x, y):
	setr(regs, x, getr(regs, x)-val(regs, y))
	
def mul(regs, x, y):
	setr(regs, x, getr(regs, x)*val(regs, y))

def mod(regs, x, y):
	setr(regs, x, getr(regs, x)%val(regs, y))

instrs = [l.split() for l in text.splitlines()]

ctr=0
def exec_instr(regs, i):
	instr = instrs[i]
	cmd, args = instr[0], instr[1:]
	if cmd == "mul":
		global ctr
		ctr += 1
	if cmd == "jnz":
		x,y = args
		if val(regs, x) != 0:
			return i+ val(regs, y)
	elif cmd == "jgz":
		x,y = args
		if val(regs, x) > 0:
			return i+ val(regs, y)
	else:
		globals()[cmd](regs, *args)
	return i+1

regs = {}
nxt = 0
cnt = 0
while nxt < len(instrs):
	cnt += 1
	nxt = exec_instr(regs, nxt)

print(len(instrs))
print(cnt)
print(regs["h"])
