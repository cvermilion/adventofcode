text = """4	10	4	1	8	4	9	14	5	1	14	15	0	15	3	5"""
blocks = list(map(int, text.split()))

def distribute(blocks, start, n):
	if n == 0:
		return
	
	start = start % len(blocks)
	blocks[start] += 1
	
	distribute(blocks, start+1, n-1)

def maxi(blocks):
	return max(enumerate(blocks), key=lambda x: x[1])[0]

def s(blocks):
	return ",".join(map(str, blocks))

ctr=0
seen = {}
nxt=s(blocks)

while not nxt in seen:
	seen[nxt] = ctr
	i = maxi(blocks)
	n = blocks[i]
	blocks[i] = 0
	distribute(blocks, i+1, n)
	nxt = s(blocks)
	ctr+=1

print(ctr-seen[nxt])
