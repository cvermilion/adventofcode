# a manual disassembly of the instructions
x=2176960
y=16777215
z=65899

def f(r3, r4):
	return y & (z * (y & (r3 + (r4 & 0xff))))

r3 = 0
r0 = 11474091
seen = set()
order = []
while r3 not in seen:
	seen.add(r3)
	order.append(r3)
	r4 = r3 | 2**16
	r3 = x
	r3 = f(r3, r4)
	#print(r3, r4)
	while r4 >= 256:
		r4 = int(r4/256)
		r3 = f(r3, r4)
		#print(r3,r4)

print(order[-1])
		

