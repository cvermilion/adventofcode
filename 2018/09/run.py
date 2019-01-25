import numpy as np

def norm_i(cir, i):
	return i % len(cir)
	
def insert(cir, i, n):
	return (cir[:i] + [n] + cir[i:])

def remove(cir, i):
	return(cir[:i] + cir[i+1:])

#nplayers = 413
#maxm = 71082

nplayers=10
maxm=1618

cir = [0]
scores = [0 for i in range(nplayers)]
cur = 0

# first loop
for i in range(1,23):
	cur = norm_i(cir, cur+2)
	cir = insert(cir, cur, i)
	
i=23
player=i%nplayers
scores[player] += i
cur = norm_i(cir, cur-7)
scores[player] += cir[cur]
print("+",cir[cur])
cir = remove(cir, cur)
print(cur, len(cir))

loops = (maxm/23) - 1
for n in range(loops):
	# first extend array by 22
	new_cir = [0] * (len(cir) + 22)
	# starting at cur we alternate taking from cir and inserting i
	new_cir[0] = cir[cur]
	for i in range(1,23):
		new_cir[2*i-1] = cir[norm_i(cir, cur+i)]
		marb = (n+1)*23 + i
		new_cir[2*i] = marb
		
	player = i%nplayers
	if i % 23 == 0:
		scores[player] += i
		cur = norm_i(cir, cur-7)
		scores[player] += cir[cur]
		print("+",cir[cur])
		cir = remove(cir, cur)
		print(cur, len(cir))
	else:
		cur = norm_i(cir, cur+2)
		cir = insert(cir, cur, i)
	if i % 10000 == 0:
		print(i,"/",maxm)

print(max(scores))


