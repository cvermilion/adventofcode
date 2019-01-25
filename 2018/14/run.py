cur1 = 0
cur2 = 1
seq = [3, 7]

#goal = 84601
goal = [0,8,4,6,0,1]
#goal = [5,9,4,1,4]

step = 0
out = []

#while len(seq) < goal+10:
#while seq[-1*len(goal):] != goal:
while step < 40:
	step += 1
	next = [int(c) for c in str(seq[cur1]+seq[cur2])]
	for i in next:
		seq.append(i)
	#seq += next
	old1 = cur1
	old2 = cur2
	cur1 = (cur1 + 1 + seq[cur1]) % len(seq)
	cur2 = (cur2 + 1 + seq[cur2]) % len(seq)
	
	print(cur1, seq[cur1], cur2, seq[cur2])
	
	if cur2 < old2:
		#print(out)
		out = []
	out.append(cur2)
	
	if step % 10000 == 0:
		print(step, cur1, cur2)

#print("".join(str(i) for i in seq[goal:goal+10]))
print(len(seq) - len(goal))
