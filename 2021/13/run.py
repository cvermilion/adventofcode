data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

data = open("input.txt").read()

pt_data, fold_data = data.split("\n\n")
pts = set([(int(l[0]), int(l[1])) for l in [ll.split(",") for ll in pt_data.split("\n")]])


def rep(pts):
	xmax = max(p[0] for p in pts)
	ymax = max(p[1] for p in pts)
	return "\n".join(["".join(["#" if (i,j) in pts else "." for i in range(xmax+1)]) for j in range(ymax+1)])

# fold 1
pts1 = set([(x if x < 655 else 1310 - x, y) for (x,y) in pts])

print("Part 1:", len(pts1))

folds = [l.split(" ")[2].split("=") for l in fold_data.split("\n") if l]

for (d, n) in folds:
	n = int(n)
	if d == "x":
		pts = [(x if x < n else 2*n-x, y) for (x,y) in pts]
	else:
		pts = [(x, y if y < n else 2*n - y) for (x,y) in pts]
		
print(rep(pts))
