from ten import knot_hash

input = "hfdlxzhv"

print(knot_hash(input))

strs = ["{}-{}".format(input, i) for i in range(128)]

hashes = map(knot_hash, strs)

def hex2bin(a):
	return {
		"0": "0000",
		"1": "0001",
		"2": "0010",
		"3": "0011",
		"4": "0100",
		"5": "0101",
		"6": "0110",
		"7": "0111",
		"8": "1000",
		"9": "1001",
		"a": "1010",
		"b": "1011",
		"c": "1100",
		"d": "1101",
		"e": "1110",
		"f": "1111",
	}[a]

bin_strs = ["".join(map(hex2bin, s)) for s in hashes]

bit_matrix = [list(map(int, s)) for s in bin_strs]

print(sum([sum(l) for l in bit_matrix]))

#Assuming (i,j) is used, return list of contiguous used cells
def add_group_members(seen,cell):
	i,j = cell
	to_visit = []
	if i > 0:
		to_visit.append((i-1,j))
	if i < 127:
		to_visit.append((i+1,j))
	if j > 0:
		to_visit.append((i,j-1))
	if j < 127:
		to_visit.append((i,j+1))
	for cell in to_visit:
		if not cell in seen and bit_matrix[cell[0]][cell[1]]:
			seen.add(cell)
			add_group_members(seen, cell)

n_groups = 0
seen = set()
for i in range(128):
	for j in range(128):
		cell = (i,j)
		if bit_matrix[i][j] and not cell in seen:
			n_groups+=1
			add_group_members(seen, cell)

print(n_groups)
	
