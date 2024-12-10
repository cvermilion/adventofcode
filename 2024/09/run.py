from me import *

input = get_data_2024(9)

input = input_test

class File:
	def __init__(self, i, l, fid):
		self.idx = i
		self.len = l
		self.id = fid
	def __repr__(self):
		return repr((self.idx,self.len,self.id))
		
class Gap:
	def __init__(self, i, l):
		self.idx = i
		self.len = l
	def __repr__(self):
		return repr((self.idx,self.len))

def parse_input(input):
	idx = 0
	files = []
	gaps = []
	for i,n in enumerate(input.strip()):
		l = int(n)
		if i%2==0:
			files.append(File(idx, l, int(i/2)))
		elif l > 0:
			gaps.append(Gap(idx, l))
		idx += l
	return files, gaps

# Part 1

files, gaps = parse_input(input)

# Iterate through the gaps, moving chunks from the last file block if possible.
# extras accumulates (partially) moved file blocks.
# Since the moves can be partial, we update the files and gaps in-place.
extras = []
while gaps:
	gap = gaps[0]
	idx, l = gap.idx, gap.len
	last = files[-1]
	if idx > last.idx:
		# all remaining files are earlier than this gap: we're done
		break
	if last.len > l:
		# last file is bigger than the gap: move part of it, remove the gap
		extras.append(File(idx, l, last.id))
		last.len -= l
		gaps = gaps[1:]
	else:
		# last file isn't bigger: move all of it
		extras.append(File(idx, last.len, last.id))
		gap.idx += last.len
		gap.len -= last.len
		files = files[:-1]
		if last.len == l:
			# exactly equal: also remove the gap
			gaps = gaps[1:]

result1 = sum(sum((f.idx+i)*f.id for i in range(f.len)) for f in files+extras)

print("Part 1:", result1)
#aocd.submit(result1, part="a", day=9)

# Part 2

files, gaps = parse_input(input)

# This iteration is actually simpler, because we never split the files, just move them.
# We iterate backward through files, then forward through gaps, to move a file if
# possible to the first big enough gap, updating the gap after the move.
for file in reversed(files):
	for (i,g) in enumerate(gaps):
		if g.idx > file.idx:
			break
		if g.len >= file.len:
			file.idx = g.idx
			g.idx += file.len
			g.len -= file.len
			if g.len == 0:
				# is a zero-length gap still a gap? 🤔
				gaps = gaps[:i] + gaps[i+1:]
			break

result2 = sum(sum((f.idx+i)*f.id for i in range(f.len)) for f in files)

print("Part 2:", result2)
#aocd.submit(result2, part="b", day=9)
