text="""48/5
25/10
35/49
34/41
35/35
47/35
34/46
47/23
28/8
27/21
40/11
22/50
48/42
38/17
50/33
13/13
22/33
17/29
50/0
20/47
28/0
42/4
46/22
19/35
17/22
33/37
47/7
35/20
8/36
24/34
6/7
7/43
45/37
21/31
37/26
16/5
11/14
7/23
2/23
3/25
20/20
18/20
19/34
25/46
41/24
0/33
3/7
49/38
47/22
44/15
24/21
10/35
6/21
14/50"""

text2="""0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

bridges = [(int(x), int(y)) for (x,y) in [l.split("/") for l in text.splitlines()]]

#print(bridges)

by_port = {}
for i, b in enumerate(bridges):
	for p in b:
		if p not in by_port:
			by_port[p] = set()
		by_port[p].add(i)

#print(by_port)

def strongest(start, used):
	choices = [i for i in by_port[start] if not i in used]
	#print("choices", start, used, choices)
	if not choices:
		return 0
	out = []
	for i in choices:
		b = bridges[i]
		if b[0] == start:
			port = b[1]
		else:
			port = b[0]
		out.append((b[0]+b[1], port, i))
	return max(s + strongest(p, used.union(set([i]))) for (s, p, i) in out)

print(strongest(0, set()))

def longest(start, used):
	choices = [i for i in by_port[start] if not i in used]
	if not choices:
		return 0, 0
	out = []
	for i in choices:
		b = bridges[i]
		if b[0] == start:
			port = b[1]
		else:
			port = b[0]
		out.append((b[0]+b[1], port, i))
	best_l, best_str, best_i = 0, 0, None
	for (s, p, i) in out:
		sub_l, sub_s = longest(p, used.union(set([i])))
		full_l = sub_l + 1
		full_s = sub_s + s
		if full_l > best_l or (full_l == best_l and full_s > best_str):
			best_l, best_str, best_i = full_l, full_s, i
	return best_l, best_str

print(longest(0, set()))
