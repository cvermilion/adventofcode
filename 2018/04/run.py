from parse import parse
input = open("input.py").readlines()
fmt = "[{ts:ti}] {desc}"
data = [parse(fmt, i) for i in input]
data = sorted(data, key=lambda d:d["ts"])
print(data[:4])

fmt2 = "Guard #{id:d} begins shift"
sleeps = {}
guard = None
sleep = None
for d in data:
	ts, desc = d["ts"], d["desc"]
	if desc.startswith("G"):
		r = parse(fmt2, desc)
		guard = r["id"]
	elif desc == "falls asleep":
		sleep = ts.minute
	else:
		new_range = [sleep, ts.minute]
		ranges = sleeps.get(guard, [])
		ranges.append(new_range)
		sleeps[guard] = ranges

def total_sleep(ranges):
	return(sum(y-x for (x,y) in ranges))

totals = [[id, total_sleep(ranges)] for (id, ranges) in sleeps.items()]

max_guard = max(totals, key=lambda m:m[1])

def max_minute(guard):
	mins = [0 for i in range(60)]
	for r in sleeps[guard]:
		for m in range(r[0], r[1]):
			mins[m] += 1

	return max(enumerate(mins), key=lambda m:m[1])

print(max_minute(max_guard[0])[0] * max_guard[0])

max_mins = [[g, max_minute(g)] for g in sleeps.keys()]
max_by_min = max(max_mins, key=lambda m:m[1][1])
print(max_by_min[0] * max_by_min[1][0])
