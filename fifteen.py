facA = 16807
initA = 591
facB = 48271
initB = 393
divisor = 2147483647

def gen(fac, x, mask):
	while True:
		x *= fac
		x = x % divisor
		if x & mask == 0:
			yield x

genA = gen(facA, initA, 0x3)
genB = gen(facB, initB, 0x7)

cnt = 0
for (n, a, b) in zip(range(5000000), genA, genB):
	if (a & 0xffff) == (b & 0xffff):
		cnt += 1

print(cnt)
