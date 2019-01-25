nplayers=413
maxm=7108200
scores = [0 for n in range(nplayers)]

class Slot (object):
	def __init__(self, val, prev, next):
		self.val = val
		self.next = next
		self.prev = prev

cur = Slot(0, None, None)
cur.prev = cur
cur.next = cur

for i in range(1, maxm+1):
	if i % 23 == 0:
		to_rem = cur.prev.prev.prev.prev.prev.prev.prev
		player = i%nplayers
		scores[player] += i
		scores[player] += to_rem.val
		to_rem.prev.next = to_rem.next
		to_rem.next.prev = to_rem.prev
		cur = to_rem.next
	else:
		bef = cur.next
		aft = bef.next
		new = Slot(i, bef, aft)
		bef.next = new
		aft.prev = new
		cur = new
		
print(max(scores))
