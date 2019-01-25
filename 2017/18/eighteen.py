text="""set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 622
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19"""

text1="""set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

ctext="""snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

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

def add(regs, x, y):
	setr(regs, x, getr(regs, x)+val(regs, y))

def mul(regs, x, y):
	setr(regs, x, getr(regs, x)*val(regs, y))

def mod(regs, x, y):
	setr(regs, x, getr(regs, x)%val(regs, y))

def snd(regs, x):
	setr(regs, "SEND", val(regs, x))

def rcv(regs, x):
	s = val(regs, x)
	if s != 0:
		set(regs, "RECV", "SEND")

instrs = [l.split() for l in text.splitlines()]

ctr=0
def exec_instr(p, regs, i):
	instr = instrs[i]
	cmd, args = instr[0], instr[1:]
	#print("exe:", cmd, args)
	if cmd == "jgz":
		x,y = args
		if val(regs, x) > 0:
			return i+ val(regs, y)
			#print("jumping to", nxt)
	else:
		globals()[cmd](regs, *args)
	if p==1 and cmd=="snd":
		global ctr
		ctr+=1
	return i+1

nxt=0
regs={}
#while getr(regs, "RECV") == 0:
#	nxt = exec_instr(0, regs, nxt)
	#print(getr("RECVD"), getr("SOUND"), regs)
	
#print(getr(regs, "RECV"))

def snd(regs, x):
	queue = getr(regs, "SEND")
	queue.append(val(regs, x))

def rcv(regs, x):
	queue = getr(regs, "RECV")
	setr(regs, x, queue.pop(0))

def stopped(regs, i):
	return len(getr(regs, "RECV")) == 0 and instrs[i][0] == "rcv"

q1 = []
q2 = []
regs1 = {"p": 0, "SEND": q1, "RECV": q2}
regs2 = {"p": 1, "SEND": q2, "RECV": q1}
i1=0
i2=0

# double prog loop
while not (stopped(regs1, i1) and stopped(regs2, i2)):
	while not stopped(regs1, i1):
		i1 = exec_instr(0, regs1, i1)
	#print("0 stopped")
	while not stopped(regs2, i2):
		i2 = exec_instr(1, regs2, i2)
	#print("1 stopped")

print(ctr)
