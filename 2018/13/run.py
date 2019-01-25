input = open("input.txt").readlines()
input[-1] += " " * (len(input[0]) - len(input[-1]))
print(input[0])

grid = [[input[j][i] for j in range(len(input))] for i in range(len(input[0]))]

print("\n".join("".join(grid[i][j] for i in range(20)) for j in range(100)))

cars = []
replacements = {
	"^": "|",
	"v": "|",
	"<": "-",
	">": "-"
}
dirs = {
	"^": "u",
	"v": "d",
	"<": "l",
	">": "r"
}
for i in range(len(grid)):
	for j in range(len(grid[0])):
		val = grid[i][j]
		if val in replacements:
			dir = dirs[val]
			grid[i][j] = replacements[val]
			cars.append([(i,j), dir, -1])

print(cars)

tick = 0
while len(cars) > 1:
	tick += 1
	cars = sorted(cars)
	locs = dict((car[0],idx) for (idx,car) in enumerate(cars))
	collided = set()
	for idx,car in enumerate(cars):
		i,j = car[0]
		dir = car[1]
		val = grid[i][j]
		next = (0,0)
		if dir == "u":
			next = i,j-1
		elif dir == "d":
			next = i,j+1
		elif dir == "r":
			next = i+1,j
		elif dir == "l":
			next = i-1,j
		next_val = grid[next[0]][next[1]]
		next_dir = dir
		next_int_dir = car[2]
		if next_val == "/":
			next_dir = {"r": "u", "u": "r", "l": "d", "d": "l"}[dir]
		elif next_val == "\\":
			next_dir = {"r": "d", "d": "r", "l": "u", "u": "l"}[dir]
		elif next_val == "+":
			if car[2] != 0:
				all_dirs = ["l", "u", "r","d"]
				
				next_dir = all_dirs[(all_dirs.index(dir) + car[2])%4]
			next_int_dir = {-1:0,0:1,1:-1}[car[2]]
		
		new_car = [next,next_dir,next_int_dir]
		if next in locs:
			print(next)
			collided.add(idx)
			collided.add(locs[next])
		else:
			cars[idx] = new_car
			locs[next] = idx
			del(locs[car[0]])
	
	cars = [c for (i,c) in enumerate(cars) if not i in collided]
print(cars)
