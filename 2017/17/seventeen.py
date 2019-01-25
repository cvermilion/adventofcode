l = 329

def step(buf, cur, n):
	nxt = (cur + l) % len(buf) + 1
	buf.insert(nxt, n)
	return nxt

buf = [0]
nxt = 0
for i in range(1,2018):
	nxt = step(buf, nxt, i)

print(buf[buf.index(2017)+1])

# For 50m case, just track current pos and 0 follower
after0 = 0
cur = 0
for size in range(1, 50000000):
	cur = (cur + l) % size
	if cur == 0:
		after0 = i
	cur += 1

print(after0)
	
