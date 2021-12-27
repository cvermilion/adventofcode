data = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".splitlines()

data = open("input2.py").readlines()

from parse import parse

instrs = [parse("{sgn} x={x1:d}..{x2:d},y={y1:d}..{y2:d},z={z1:d}..{z2:d}", l) for l in data]

#print(instrs[:-2])
pts = [[[0,0] for j in range(101)] for i in range(101)]

part = 23
for instr in instrs:
	x1,x2 = sorted([instr["x1"], instr["x2"]])
	y1,y2 = sorted([instr["y1"], instr["y2"]])
	z1,z2 = sorted([instr["z1"], instr["z2"]])
	x1,y1,z1 = map(lambda n: max([-50, n]), [x1,y1,z1])
	x2,y2,z2 = map(lambda n: min([50, n]), [x2,y2,z2])
	on = instr["sgn"] == "on"
	posmask, negmask = None, None
	if z2 >= 0 and z1 <= 50:
		posmask = sum(1<<z for z in range(max([0, z1]), z2+1))
		invposmask = 0xffffffffffffffff - posmask
	if z1 < 0 and z2 >= -50:
		negmask = sum(1<<z for z in range(-min([-1,z2]), -z1+1))
		invnegmask = 0xffffffffffffffff - negmask
	for i in range(x1+50, x2+51):
		for j in range(y1+50, y2+51):
			if posmask:
				if on:
					pts[j][i][0] |= posmask
				else:
					pts[j][i][0] &= invposmask
			if negmask:
				if on:
					pts[j][i][1] |= negmask
				else:
					pts[j][i][1] &= invnegmask

def sum_bits(b):
	return sum(map(int, "{:b}".format(b)))

def allon(pts):
	return sum(sum(sum_bits(pos)+sum_bits(neg) for [pos,neg] in row) for row in pts)

print(allon(pts))
