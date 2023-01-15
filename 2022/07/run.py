import os, sys
sys.path.append(os.path.realpath(".."))
from util import *

#test()
input = get_input()

steps = [s.splitlines() for s in input.split("$") if s != ""]
steps = [[l.strip() for l in step] for step in steps]

fs = {"sub": {}, "files": {}}
pwd = ()
cur = fs

# build fs
for step in steps:
	if step[0].startswith("cd "):
		dir = step[0][3:]
		if dir == "/":
			pwd = ()
			cur = fs
		elif dir == "..":
			pwd = pwd[:-1]
			cur = fs
			for d in pwd:
				cur = cur["sub"][d]
		else:
			pwd = pwd + (dir,)
			if dir not in cur["sub"]:
				cur["sub"][dir] = {"sub":{},"files":{}}
			cur = cur["sub"][dir]
	
	else:
		# ls
		for line in step[1:]:
			if not line.startswith("dir"):
				size, file = line.split(" ")
				path = pwd + (file,)
				cur["files"][file] = int(size)


to_delete = 100000000000

def totals(dir):
	files = sum(dir["files"].values())
	dirs = list(map(totals, dir["sub"].values()))
	my_total = files + sum(d[0] for d in dirs)
	big_total = sum(d[1] for d in dirs)
	if my_total <= 100000:
		big_total += my_total
	
	# part 2
	global to_delete
	if my_total < to_delete and my_total > 8381165:
		to_delete = my_total
	
	return my_total, big_total

print("Part 1:", totals(fs)[1])

print("Part 2:", to_delete)
