class Node (object):
	def __init__(self, idx, val):
		self.idx = idx
		self.val = val
		self.next = None

init = [3,7,1,0,1,0,1,2,4,5]

n0 = Node(0,3)
n1 = Node(1,7)
#n0.next = n1
#n1.next = n2

cur1=n0
cur2=n1

first24 = [n0,n1]
while len(first24) < 24:
	next = [int(c) for c in str(cur1.val+cur2.val)]
	for i in next:
		first24.append(Node(len(first24), i))

	cur1 = first24[(cur1.idx + cur1.val + 1) % len(first24)]
	cur2 = first24[(cur2.idx + cur2.val + 1) % len(first24)]

print([n.val for n in first24])
print(len(first24))

for (i,n) in enumerate(first24):
	next_idx  = (i + (1 + n.val)) % len(first24)
	n.next = first24[next_idx]

last_node = first24[23]
next_last_jmp = last_node.val
following = []

total=24
#last6 = [n.val for n in first24[-6:]]
goal = [0,8,4,6,0,1]
#goal = [5,9,4,1,4]
last = [n.val for n in first24[-len(goal):]]

while last != goal:
	#print(cur1.idx, cur1.val, cur2.idx, cur2.val, last_node.idx, following, last)
	next = [int(c) for c in str(cur1.val+cur2.val)]
	for i in next:		
		following.append(i)
		last.append(i)
		last = last[1:]
		total += 1
		if last == goal:
			break
	
	while len(following) > next_last_jmp:
		next_last_node = Node(last_node.idx + next_last_jmp+1, following[next_last_jmp])
		last_node.next = next_last_node
		last_node = next_last_node
		following = following[next_last_jmp+1:]
		next_last_jmp = last_node.val
		
	last_node.next = first24[last_node.val - len(following)]
	
	cur1 = cur1.next
	cur2 = cur2.next

#print(total, following, last)
print(total - len(goal))
	
	

